import scrapy
import logging
from scrapy_playwright.page import PageMethod
from sece_scraper.helpers.pdf_processor import PDFProcessor
from sece_scraper.helpers.image_processor import ImageProcessor
from sece_scraper.helpers.faculty_scraper import FacultyScraper
from sece_scraper.helpers.data_cleaner import DataCleaner
from sece_scraper.utils.storage import JSONLStorage

logger = logging.getLogger(__name__)

class SECEMasterSpider(scrapy.Spider):
    """
    Deep web scraper for SECE CSE Department
    Extracts syllabi, events, and achievements with OCR and PDF processing
    """
    
    name = "sece_deep_crawl"
    allowed_domains = ["sece.ac.in"]
    start_urls = ["https://sece.ac.in/department-computer-science-engineering-2/"]
    
    # Page interaction settings
    WAIT_TIME = 2000  # milliseconds
    YEAR_BUTTONS = ["2023", "2022", "2021", "2020", "2019"]
    
    def __init__(self, *args, **kwargs):
        super(SECEMasterSpider, self).__init__(*args, **kwargs)
        self.image_processor = ImageProcessor()
        self.pdf_processor = PDFProcessor()
        self.faculty_scraper = FacultyScraper()
        self.seen_content = set()
    
    def start_requests(self):
        """Initial request to CSE main page"""
        logger.info("Starting SECE CSE scraper")
        
        yield scrapy.Request(
            self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    # Wait for page to load
                    PageMethod("wait_for_load_state", "networkidle"),
                ]
            },
            callback=self.parse_main,
            errback=self.errback_main
        )
    
    def parse_main(self, response):
        """
        Parse main CSE department page
        - Extract syllabus PDF links
        - Extract faculty information
        - Extract HOD information
        - Look for curriculum/dropdown elements
        """
        logger.info("Parsing main CSE department page")
        
        # 1. Extract Faculty Information
        faculty_list = self.faculty_scraper.extract_faculty_info(response)
        for faculty_item in faculty_list:
            yield faculty_item
        
        # 2. Extract HOD Information
        hod_info = self.faculty_scraper.extract_hod_info(response)
        if hod_info:
            yield hod_info
        
        # 3. Extract PDF Links (Syllabi)
        pdf_links = response.css("a[href*='drive.google.com']::attr(href)").getall()
        logger.info(f"Found {len(pdf_links)} PDF links")
        
        for pdf_url in pdf_links:
            if pdf_url not in self.seen_content:
                self.seen_content.add(pdf_url)
                
                # Extract text from PDF
                text = self.pdf_processor.process_pdf_url(pdf_url)
                if text:
                    yield {
                        "type": "syllabus",
                        "source_url": response.url,
                        "data": text,
                        "original_link": pdf_url,
                    }
        
        # 4. Extract Placement Statistics (from the page)
        for stat_item in self.parse_placement_stats(response):
            yield stat_item
        
        # 5. Look for all internal links on the page
        internal_links = response.css("a::attr(href)").getall()
        
        # Filter for relevant pages
        relevant_paths = ["/events/", "/cse-student-achievements/", "/curriculum/", "/academics/", "/recruiters/"]
        
        for link in internal_links:
            if any(path in link for path in relevant_paths):
                absolute_url = response.urljoin(link)
                if absolute_url not in self.seen_content:
                    self.seen_content.add(absolute_url)
                    yield scrapy.Request(
                        absolute_url,
                        meta={
                            "playwright": True,
                            "playwright_include_page": True,
                            "playwright_page_methods": [
                                PageMethod("wait_for_load_state", "networkidle"),
                            ]
                        },
                        callback=self.parse_subpage,
                        errback=self.errback_subpage
                    )
    
    def parse_placement_stats(self, response):
        """
        Extract placement statistics from the CSE department page
        Looks for key stats like total intake, highest salary, recruiter count
        """
        logger.info("Extracting placement statistics")
        
        # Look for stats in common patterns
        stats_text = response.xpath("//text()[contains(., 'TOTAL INTAKE') or contains(., 'HIGHEST SALARY') or contains(., 'RECRUITERS')]").getall()
        
        if stats_text:
            stats_content = " ".join(stats_text)
            if len(stats_content) > 50:
                yield {
                    "type": "placement_stat",
                    "source_url": response.url,
                    "data": stats_content,
                    "content_type": "text",
                }
    
    def parse_subpage(self, response):
        """
        Parse subpages (Events, Achievements, Recruiters, etc.)
        - Handle year-wise button clicks
        - Extract images and apply OCR
        - Extract text content
        - Handle recruiter logos
        - Handle testimonial carousels
        """
        page_title = response.xpath("//h1/text()").get()
        logger.info(f"Parsing subpage: {page_title}")
        
        # Determine page type
        page_type = "unknown"
        if "events" in response.url.lower():
            page_type = "event"
        elif "achievement" in response.url.lower():
            page_type = "achievement"
        elif "curriculum" in response.url.lower() or "academics" in response.url.lower():
            page_type = "curriculum"
        elif "recruiter" in response.url.lower():
            page_type = "recruiter"
            # Handle recruiter logos
            for recruiter_item in self.extract_recruiter_logos(response):
                yield recruiter_item
            return
        
        # 1. Extract images and apply OCR (for events/achievements)
        image_urls = response.css("img::attr(src)").getall()
        logger.info(f"Found {len(image_urls)} images")
        
        for img_url in image_urls:
            absolute_img_url = response.urljoin(img_url)
            if absolute_img_url not in self.seen_content:
                self.seen_content.add(absolute_img_url)
                
                # Apply OCR
                ocr_text = self.image_processor.extract_text_from_image(absolute_img_url)
                if ocr_text:
                    yield {
                        "type": page_type,
                        "source_url": response.url,
                        "data": ocr_text,
                        "image_url": absolute_img_url,
                    }
        
        # 2. Extract text content
        main_content = response.css(".entry-content, .page-content, main, article").get()
        if main_content:
            text_content = scrapy.Selector(text=main_content).css("::text").getall()
            full_text = " ".join([t.strip() for t in text_content if t.strip()])
            
            if full_text and len(full_text) > 100:
                content_hash = hash(full_text)
                if content_hash not in self.seen_content:
                    self.seen_content.add(content_hash)
                    yield {
                        "type": page_type,
                        "source_url": response.url,
                        "data": full_text,
                        "content_type": "text",
                    }
        
        # 3. Handle testimonial carousels (if on achievements/alumni page)
        if "achievement" in response.url.lower() or "alumni" in response.url.lower():
            for testimonial_item in self.extract_testimonials(response):
                yield testimonial_item
        
        # 4. Look for year-wise buttons and handle clicks
        # This would require additional Playwright handling in a production environment
        self.handle_year_buttons(response, page_type)
    
    def extract_recruiter_logos(self, response):
        """
        Extract recruiter company logos and names from recruiters page
        """
        logger.info("Extracting recruiter logos")
        
        # Find all recruiter items (usually in a grid/carousel)
        recruiter_items = response.css(".recruiter-item, .company-logo, .recruiter, [data-recruiter]")  
        
        for item in recruiter_items:
            # Extract logo image
            logo_url = item.css("img::attr(src)").get()
            company_name = item.css("img::attr(alt), .company-name::text").get()
            
            if logo_url:
                absolute_logo_url = response.urljoin(logo_url)
                if absolute_logo_url not in self.seen_content:
                    self.seen_content.add(absolute_logo_url)
                    
                    yield {
                        "type": "recruiter",
                        "source_url": response.url,
                        "company_name": company_name or "Unknown",
                        "logo_url": absolute_logo_url,
                        "data": company_name or logo_url,
                    }
    
    def extract_testimonials(self, response):
        """
        Extract alumni testimonials from carousel/sliding images
        Uses OCR to extract text from testimonial images
        """
        logger.info("Extracting alumni testimonials")
        
        # Find testimonial carousel items (usually have specific CSS classes)
        testimonial_items = response.css(".testimonial, .alumni-testimonial, .slide, [data-testimonial]")
        
        for item in testimonial_items:
            # Try to find image in testimonial
            img_url = item.css("img::attr(src)").get()
            
            if img_url:
                absolute_img_url = response.urljoin(img_url)
                if absolute_img_url not in self.seen_content:
                    self.seen_content.add(absolute_img_url)
                    
                    # Apply OCR to extract testimonial text
                    ocr_text = self.image_processor.extract_text_from_image(absolute_img_url)
                    if ocr_text:
                        yield {
                            "type": "testimonial",
                            "source_url": response.url,
                            "data": ocr_text,
                            "image_url": absolute_img_url,
                        }
            else:
                # If no image, try to extract text directly
                text_content = item.css("::text").getall()
                full_text = " ".join([t.strip() for t in text_content if t.strip()])
                
                if full_text and len(full_text) > 50:
                    content_hash = hash(full_text)
                    if content_hash not in self.seen_content:
                        self.seen_content.add(content_hash)
                        yield {
                            "type": "testimonial",
                            "source_url": response.url,
                            "data": full_text,
                        }
    
    def handle_year_buttons(self, response, page_type):
        """
        Handle year-wise button clicks
        In production, use Playwright to click buttons and re-scrape
        """
        # Check if year buttons exist
        year_buttons = response.css("button, .year-button, .filter-year")
        
        if year_buttons:
            logger.info(f"Found year buttons, would need Playwright interaction for full extraction")
            # In production: use PageMethod to click each button and wait for content
    
    def closed(self, reason):
        """Spider closing handler"""
        logger.info(f"Spider closed: {reason}")
        
        # Print statistics
        stats = JSONLStorage.get_file_stats(self.settings.get('DATA_RAW_PATH'))
        if stats:
            logger.info(f"Stored {stats.get('lines', 0)} items in raw data file")
    
    def errback_main(self, failure):
        """Error handler for main page"""
        logger.error(f"Error on main page: {failure.value}")
    
    def errback_subpage(self, failure):
        """Error handler for subpages"""
        logger.error(f"Error on subpage: {failure.value}")
