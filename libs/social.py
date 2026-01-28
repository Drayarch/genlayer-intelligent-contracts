"""
Social Media / Web Scraping Library for GenLayer Intelligent Contracts

This library provides reusable functions for web scraping and content analysis.
Can be imported by multiple contracts.

Usage:
    from libs.social import scrape_webpage, search_text, extract_links
"""

from typing import List, Dict, Any
import re


def scrape_webpage(url: str, gl_get_webpage, mode: str = 'text') -> str:
    """
    Scrape content from a webpage.
    
    Args:
        url (str): URL to scrape
        gl_get_webpage: GenLayer's get_webpage function
        mode (str): 'text' or 'html'
        
    Returns:
        str: Webpage content
        
    Example:
        content = scrape_webpage("https://example.com", gl.get_webpage)
    """
    return gl_get_webpage(url, mode=mode)


def scrape_limited(url: str, gl_get_webpage, max_chars: int = 500) -> str:
    """
    Scrape webpage with character limit.
    
    Args:
        url (str): URL to scrape
        gl_get_webpage: GenLayer's get_webpage function
        max_chars (int): Maximum characters to return
        
    Returns:
        str: Limited webpage content
        
    Example:
        snippet = scrape_limited("https://example.com", gl.get_webpage, 200)
    """
    content = gl_get_webpage(url, mode='text')
    return content[:max_chars]


def search_text(content: str, search_term: str, case_sensitive: bool = False) -> bool:
    """
    Search for a term in webpage content.
    
    Args:
        content (str): Text content to search
        search_term (str): Term to find
        case_sensitive (bool): Whether search is case-sensitive
        
    Returns:
        bool: True if term found, False otherwise
        
    Example:
        found = search_text(content, "blockchain")
    """
    if not case_sensitive:
        return search_term.lower() in content.lower()
    return search_term in content


def count_occurrences(content: str, search_term: str) -> int:
    """
    Count how many times a term appears in content.
    
    Args:
        content (str): Text content
        search_term (str): Term to count
        
    Returns:
        int: Number of occurrences
        
    Example:
        count = count_occurrences(content, "GenLayer")
    """
    return content.lower().count(search_term.lower())


def extract_emails(content: str) -> List[str]:
    """
    Extract email addresses from content.
    
    Args:
        content (str): Text content
        
    Returns:
        list: List of email addresses found
        
    Example:
        emails = extract_emails(content)
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, content)


def extract_urls(content: str) -> List[str]:
    """
    Extract URLs from content.
    
    Args:
        content (str): Text content
        
    Returns:
        list: List of URLs found
        
    Example:
        urls = extract_urls(content)
    """
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, content)


def get_word_count(content: str) -> int:
    """
    Count words in content.
    
    Args:
        content (str): Text content
        
    Returns:
        int: Number of words
        
    Example:
        words = get_word_count(content)
    """
    return len(content.split())


def extract_hashtags(content: str) -> List[str]:
    """
    Extract hashtags from social media content.
    
    Args:
        content (str): Text content
        
    Returns:
        list: List of hashtags found
        
    Example:
        tags = extract_hashtags("#GenLayer is amazing! #blockchain")
        # Returns: ['GenLayer', 'blockchain']
    """
    hashtag_pattern = r'#(\w+)'
    return re.findall(hashtag_pattern, content)


def extract_mentions(content: str) -> List[str]:
    """
    Extract @mentions from social media content.
    
    Args:
        content (str): Text content
        
    Returns:
        list: List of mentions found
        
    Example:
        mentions = extract_mentions("Hey @user1 and @user2!")
        # Returns: ['user1', 'user2']
    """
    mention_pattern = r'@(\w+)'
    return re.findall(mention_pattern, content)


def clean_text(content: str) -> str:
    """
    Clean text by removing extra whitespace and special characters.
    
    Args:
        content (str): Raw text content
        
    Returns:
        str: Cleaned text
        
    Example:
        clean = clean_text("  Hello   World!  ")
        # Returns: "Hello World!"
    """
    # Remove extra whitespace
    content = ' '.join(content.split())
    # Remove special characters (keep alphanumeric and basic punctuation)
    content = re.sub(r'[^\w\s.,!?-]', '', content)
    return content.strip()


def summarize_content(content: str, max_length: int = 100) -> str:
    """
    Create a short summary of content.
    
    Args:
        content (str): Full text content
        max_length (int): Maximum summary length
        
    Returns:
        str: Summarized content
        
    Example:
        summary = summarize_content(long_text, 50)
    """
    if len(content) <= max_length:
        return content
    return content[:max_length].rsplit(' ', 1)[0] + '...'


def contains_keywords(content: str, keywords: List[str]) -> Dict[str, bool]:
    """
    Check if content contains specific keywords.
    
    Args:
        content (str): Text content
        keywords (list): List of keywords to check
        
    Returns:
        dict: Dictionary showing which keywords were found
        
    Example:
        result = contains_keywords(content, ['blockchain', 'AI', 'crypto'])
        # Returns: {'blockchain': True, 'AI': False, 'crypto': True}
    """
    content_lower = content.lower()
    return {keyword: keyword.lower() in content_lower for keyword in keywords}


def get_sentiment_keywords() -> Dict[str, List[str]]:
    """
    Get predefined sentiment keywords for basic sentiment analysis.
    
    Returns:
        dict: Dictionary of positive and negative keywords
        
    Example:
        keywords = get_sentiment_keywords()
    """
    return {
        'positive': ['good', 'great', 'excellent', 'amazing', 'awesome', 'love', 'best', 'wonderful'],
        'negative': ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointing', 'poor']
    }


def basic_sentiment_analysis(content: str) -> str:
    """
    Perform basic sentiment analysis on content.
    
    Args:
        content (str): Text content
        
    Returns:
        str: 'positive', 'negative', or 'neutral'
        
    Example:
        sentiment = basic_sentiment_analysis("This is amazing!")
        # Returns: 'positive'
    """
    keywords = get_sentiment_keywords()
    content_lower = content.lower()
    
    positive_count = sum(1 for word in keywords['positive'] if word in content_lower)
    negative_count = sum(1 for word in keywords['negative'] if word in content_lower)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'


# Common social media platforms
SOCIAL_PLATFORMS = {
    'twitter': 'twitter.com',
    'facebook': 'facebook.com',
    'instagram': 'instagram.com',
    'linkedin': 'linkedin.com',
    'reddit': 'reddit.com',
    'youtube': 'youtube.com'
}


def identify_platform(url: str) -> str:
    """
    Identify social media platform from URL.
    
    Args:
        url (str): URL to check
        
    Returns:
        str: Platform name or 'unknown'
        
    Example:
        platform = identify_platform("https://twitter.com/user")
        # Returns: 'twitter'
    """
    url_lower = url.lower()
    for platform, domain in SOCIAL_PLATFORMS.items():
        if domain in url_lower:
            return platform
    return 'unknown'
