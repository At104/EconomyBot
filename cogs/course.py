import discord
from discord.ext import commands
from discord.commands import slash_command
import aiohttp
import re
from bs4 import BeautifulSoup
import ssl


class Course(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Look up course information from McMaster University's course directory")
    async def course(self, ctx, course_code: str = discord.Option(description="Course code (e.g., MATH1ZB3, COMPSCI2C03)")):
        """
        Look up course information from McMaster's course directory
        Usage: /course MATH1ZB3 or /course "MATH 1ZB3"
        """
        # Clean up the course code
        course_code = course_code.upper().replace(" ", "")
        
        # Parse course code (e.g., MATH1ZB3 -> MATH and 1ZB3)
        match = re.match(r'([A-Z]+)(\d+[A-Z]*\d*)', course_code)
        if not match:
            await ctx.respond("❌ Invalid course code format. Please use format like MATH1ZB3 or COMPSCI2C03")
            return
        
        subject = match.group(1)
        course_num = match.group(2)
        
        print(f"Searching up course {subject} {course_num}")
        
        try:
            await ctx.defer()
            
            course_info = await self.scrape_mcmaster_course(subject, course_num)
            
            if course_info:
                # Build the formatted text with proper line breaks
                lines = []
                lines.append(f"## **{course_info['code']} - {course_info['title']}**")
                lines.append(f"**{course_info['units']}**")
                if course_info['description']:
                    lines.append(course_info['description'])
                if course_info['schedule']:
                    lines.append(course_info['schedule'])
                if course_info['prerequisites']:
                    lines.append(f"**Prerequisite(s):** {course_info['prerequisites']}")
                if course_info['antirequisites']:
                    lines.append(f"**Antirequisite(s):** {course_info['antirequisites']}")
                if course_info['corequisites']:
                    lines.append(f"**Co-requisite(s):** {course_info['corequisites']}")
                if course_info['crosslists']:
                    lines.append(f"**Cross-list(s):** {course_info['crosslists']}")
                if course_info['restrictions']:
                    lines.append(course_info['restrictions'])
                if course_info['admin_info']:
                    lines.append(course_info['admin_info'])
                
                formatted_text = '\n'.join(lines)
                
                embed = discord.Embed(
                    description=formatted_text,
                    color=discord.Color.from_rgb(122, 0, 60)  # McMaster maroon
                )
                embed.set_footer(text="McMaster University Course Directory")
                
                await ctx.followup.send(embed=embed)
            else:
                await ctx.followup.send(f"❌ Course **{subject} {course_num}** not found in McMaster's course directory.")
                
        except Exception as e:
            await ctx.followup.send(f"❌ Error looking up course: {str(e)}")

    async def scrape_mcmaster_course(self, subject, course_num):
        """
        Scrape course information from McMaster's course directory
        """
        try:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            timeout = aiohttp.ClientTimeout(total=20)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                # Search for the course
                search_url = "https://academiccalendars.romcmaster.ca/search_advanced.php"
                search_params = {
                    'cur_cat_oid': '58',
                    'search_database': 'Search',
                    'search_db': 'Search',
                    'cpage': '1',
                    'ecpage': '1',
                    'ppage': '1',
                    'spage': '1',
                    'tpage': '1',
                    'location': '33',
                    'filter[keyword]': f"{subject} {course_num}",
                    'filter[exact_match]': '1'
                }
                
                async with session.get(search_url, headers=headers, params=search_params) as response:
                    if response.status == 200:
                        search_html = await response.text()
                        
                        # Extract course ID
                        soup = BeautifulSoup(search_html, 'html.parser')
                        course_pattern = subject + r"\s*" + course_num
                        
                        course_id = None
                        for link in soup.find_all('a', href=True):
                            link_text = link.get_text(strip=True)
                            if re.search(course_pattern, link_text, re.IGNORECASE):
                                href = link['href']
                                match = re.search(r'coid=(\d+)', href)
                                if match:
                                    course_id = match.group(1)
                                    break
                        
                        if course_id:
                            # Get the course details page
                            course_url = f"https://academiccalendars.romcmaster.ca/preview_course.php?catoid=58&coid={course_id}"
                            
                            async with session.get(course_url, headers=headers) as course_response:
                                if course_response.status == 200:
                                    course_html = await course_response.text()
                                    return self.parse_course_details(course_html, subject, course_num)
                    
        except Exception as e:
            print(f"Error scraping McMaster course: {e}")
            
        return None

    def parse_course_details(self, html, subject, course_num):
        """
        Parse course details from McMaster's course page
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            full_text = soup.get_text()
            
            # Print the raw text so we can see what we're working with
            print("=" * 80)
            print("RAW TEXT FROM COURSE PAGE:")
            print("=" * 80)
            print(full_text)
            print("=" * 80)
            
            course_code = f"{subject} {course_num}"
            
            # Extract title
            title_match = re.search(rf'{subject} {course_num} - (.+?) \d+ unit\(s\)', full_text)
            title = title_match.group(1).strip() if title_match else None
            print(f"TITLE: {title}")
            
            # Extract units
            units_match = re.search(r'(\d+ unit\(s\))', full_text)
            units = units_match.group(1) if units_match else None
            print(f"UNITS: {units}")
            
            # Extract description - handle ALL possible schedule patterns
            desc_patterns = [
                r'Three lectures',
                r'Two lectures', 
                r'One lecture',
                r'Lectures and discussion',
                r'On-line',
                r'Tutorial',
                r'Seminar',
                r'Laboratory',
                r'Practicum',
                r'Workshop',
                r'Field work',
                r'Independent study',
                r'Thesis',
                r'Project',
                r'Clinical',
                r'Directed study',
                r'Reading course',
                r'Co-op'
            ]
            
            desc_pattern = '|'.join(desc_patterns)
            desc_match = re.search(rf'{subject} {course_num} - .+? \d+ unit\(s\) (.+?)(?:\n|\r\n|\r)(?:{desc_pattern})', full_text, re.DOTALL)
            if desc_match:
                description = desc_match.group(1).strip()
                description = re.sub(r'\s+', ' ', description)
            else:
                description = None
            print(f"DESCRIPTION: {description}")
            
            # Extract schedule - handle ALL possible patterns
            schedule_patterns = [
                r'(?:Three|Two|One|Four|Five) lectures?[^\n\r]*',
                r'Lectures and discussion[^\n\r]*',
                r'On-line[^\n\r]*',
                r'Tutorial[^\n\r]*',
                r'Seminar[^\n\r]*',
                r'Laboratory[^\n\r]*',
                r'Practicum[^\n\r]*',
                r'Workshop[^\n\r]*',
                r'Field work[^\n\r]*',
                r'Independent study[^\n\r]*',
                r'Thesis[^\n\r]*',
                r'Project[^\n\r]*',
                r'Clinical[^\n\r]*',
                r'Directed study[^\n\r]*',
                r'Reading course[^\n\r]*',
                r'Co-op[^\n\r]*'
            ]
            
            schedule_pattern = '|'.join(schedule_patterns)
            schedule_match = re.search(rf'({schedule_pattern})(?:\n|\r\n|\r)?[^\n\r]*(?:one term|two terms|fall|winter|spring|summer)', full_text, re.IGNORECASE)
            schedule = schedule_match.group(1).strip() if schedule_match else None
            print(f"SCHEDULE: {schedule}")
            
            # Extract prerequisites - handle ALL possible end patterns
            prereq_end_patterns = [
                r'Antirequisite',
                r'Cross-list', 
                r'This course',
                r'Not open',
                r'Print-Friendly',
                r'Close Window',
                r'Co-requisite',
                r'Corequisite'
            ]
            
            prereq_end_pattern = '|'.join(prereq_end_patterns)
            prereq_match = re.search(rf'Prerequisite\(s\): (.+?)(?:\n|\r\n|\r)(?:{prereq_end_pattern})', full_text)
            prerequisites = prereq_match.group(1).strip() if prereq_match else None
            print(f"PREREQUISITES: {prerequisites}")
            
            # Extract antirequisites - handle ALL possible end patterns
            antireq_end_patterns = [
                r'Cross-list',
                r'This course', 
                r'Not open',
                r'Print-Friendly',
                r'Close Window',
                r'Co-requisite',
                r'Corequisite'
            ]
            
            antireq_end_pattern = '|'.join(antireq_end_patterns)
            antireq_match = re.search(rf'Antirequisite\(s\): (.+?)(?:\n|\r\n|\r)(?:{antireq_end_pattern})', full_text)
            antirequisites = antireq_match.group(1).strip() if antireq_match else None
            print(f"ANTIREQUISITES: {antirequisites}")
            
            # Extract corequisites
            coreq_match = re.search(rf'(?:Co-requisite|Corequisite)\(s\): (.+?)(?:\n|\r\n|\r)', full_text)
            corequisites = coreq_match.group(1).strip() if coreq_match else None
            print(f"COREQUISITES: {corequisites}")
            
            # Extract cross-lists
            crosslist_match = re.search(r'Cross-list\(s\): (.+?)(?:\n|\r\n|\r)', full_text)
            crosslists = crosslist_match.group(1).strip() if crosslist_match else None
            print(f"CROSS-LISTS: {crosslists}")
            
            # Extract additional info
            admin_match = re.search(r'(This course is administered by .+?)(?:\n|\r\n|\r)', full_text)
            admin_info = admin_match.group(1).strip() if admin_match else None
            print(f"ADMIN INFO: {admin_info}")
            
            # Extract restrictions - comprehensive pattern
            restrict_match = re.search(r'(Not open to students.+?)(?:Print-Friendly|Close Window|All calendars)', full_text, re.DOTALL)
            if restrict_match:
                restrictions = restrict_match.group(1).strip()
                restrictions = re.sub(r'\s+', ' ', restrictions)
            else:
                restrictions = None
            print(f"RESTRICTIONS: {restrictions}")
            
            return {
                'code': course_code,
                'title': title,
                'units': units,
                'description': description,
                'schedule': schedule,
                'prerequisites': prerequisites,
                'antirequisites': antirequisites,
                'corequisites': corequisites,
                'restrictions': restrictions,
                'crosslists': crosslists,
                'admin_info': admin_info
            }
                
        except Exception as e:
            print(f"Error parsing course details: {e}")
            return None

def setup(bot):
    bot.add_cog(Course(bot))
