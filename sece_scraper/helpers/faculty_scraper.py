"""
Faculty Profile Scraper
Extracts faculty and HOD information from SECE CSE department page
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class FacultyScraper:
    """Handles extraction of faculty and HOD information"""
    
    def __init__(self):
        self.seen_faculty = set()
    
    def extract_faculty_info(self, response) -> List[Dict]:
        """
        Extract faculty information from CSE department page
        Looks for faculty member names, titles, qualifications, specializations
        """
        logger.info("Extracting faculty information")
        faculty_list = []
        
        # SECE uses Elementor framework with divs containing h2 > a with faculty names
        # Get all faculty item containers (divs with h2 containing faculty links)
        faculty_items = response.xpath('//div[@class="elementor-widget-container"]/h2[a[contains(text(), "Dr.") or contains(text(), "Mr.") or contains(text(), "Ms.") or contains(text(), "Prof")]]/../../..')
        
        logger.info(f"Found {len(faculty_items)} faculty items")
        
        for item in faculty_items:
            faculty_info = self.parse_faculty_item(item, response.url)
            if faculty_info:
                faculty_list.append(faculty_info)
        
        return faculty_list
    
    def parse_faculty_item(self, item, source_url: str) -> Optional[Dict]:
        """
        Parse individual faculty item from Elementor container
        Extracts: name, title
        """
        try:
            # SECE structure: div container > div > h2 > a (name) + p (title)
            # Extract name from link
            name_link = item.xpath('.//h2//a[1]')
            if not name_link:
                return None
                
            name = name_link[0].xpath('./text()').get()
            if not name:
                return None
            
            # Check if already seen
            if name in self.seen_faculty:
                return None
            
            self.seen_faculty.add(name)
            
            # Extract title from paragraph following the heading
            title = item.xpath('.//h2/following-sibling::p[1]/text()').get()
            
            # Extract image if present
            image_url = item.xpath('.//img/@src').get()
            
            # Extract profile link
            profile_link = item.xpath('.//h2//a/@href').get()
            
            # Format the extracted data
            faculty_data = self._format_faculty_data(
                name=name,
                title=title or "",
            )
            
            return {
                "type": "faculty",
                "source_url": source_url,
                "name": name.strip(),
                "title": (title.strip() if title else "Faculty Member"),
                "data": faculty_data,
                "image_url": image_url,
                "profile_url": profile_link,
            }
            
        except Exception as e:
            logger.error(f"Error parsing faculty item: {e}")
            return None
    
    def _format_faculty_data(self, name: str, title: str) -> str:
        """Format faculty information into structured text"""
        parts = [f"Name: {name}"]
        
        if title:
            parts.append(f"Title: {title}")
        
        return "\n".join(parts)
    
    def extract_hod_info(self, response) -> Optional[Dict]:
        """
        Extract Head of Department (HOD) information
        Uses XPath to find HOD section after heading
        """
        logger.info("Extracting HOD information")
        
        # Find the HOD section heading and get the following sibling container
        hod_container = response.xpath('//h2[text()="Head of the department"]/parent::div/following-sibling::div[1]')
        
        if not hod_container:
            logger.info("HOD container not found")
            return None
        
        try:
            # Extract HOD name from h2 in the container
            hod_name = hod_container.xpath('.//h2//a/text()').get()
            if not hod_name:
                hod_name = hod_container.xpath('.//h2/text()').get()
            
            if not hod_name:
                return None
            
            # Extract HOD title from paragraph
            hod_title = hod_container.xpath('.//p/text()').get()
            
            # Extract image
            hod_image = hod_container.xpath('.//img/@src').get()
            
            # Extract profile link
            hod_link = hod_container.xpath('.//h2//a/@href').get()
            
            hod_data = self._format_faculty_data(hod_name.strip(), (hod_title.strip() if hod_title else "Head of the Department"))
            
            return {
                "type": "hod",
                "source_url": response.url,
                "name": hod_name.strip(),
                "title": (hod_title.strip() if hod_title else "Head of the Department"),
                "data": hod_data,
                "image_url": hod_image,
                "profile_url": hod_link,
            }
            
        except Exception as e:
            logger.error(f"Error parsing HOD info: {e}")
            return None

