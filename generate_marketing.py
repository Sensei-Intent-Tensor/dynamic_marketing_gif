#!/usr/bin/env python3
"""
Dynamic Marketing GIF Generator
Full-spectrum marketing frame generation with complete customization
"""

import hashlib
import math
import random
import colorsys

# Default text values
DEFAULT_COMPANY = "Auto_Workspace-AI"
DEFAULT_SERVICES = ["Expert Consulting", "AI Automations", "Live Workshops"]

# Font styles
FONT_STYLES = {
    'bold': {
        'family': 'Arial Black, sans-serif',
        'weight': 'bold',
        'spacing': '2px'
    },
    'tech': {
        'family': 'Courier New, monospace',
        'weight': 'bold',
        'spacing': '3px'
    },
    'elegant': {
        'family': 'Georgia, serif',
        'weight': 'normal',
        'spacing': '1px'
    },
    'blocky': {
        'family': 'Impact, sans-serif',
        'weight': 'bold',
        'spacing': '0px'
    },
    'script': {
        'family': 'Brush Script MT, cursive',
        'weight': 'normal',
        'spacing': '1px'
    }
}

# Geometry patterns
GEOMETRY_PATTERNS = ['sharp', 'round', 'mixed', 'minimal']

# Background gradient styles
BG_STYLES = [
    'vertical',      # Top to bottom
    'diagonal',      # Corner to corner
    'radial',        # Center outward
    'horizontal',    # Left to right
    'double',        # Two-tone split
    'triple'         # Three-color gradient
]

def hsl_to_rgb(h, s, l):
    """Convert HSL to RGB hex color"""
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

def calculate_luminance(hex_color):
    """Calculate relative luminance for contrast checking"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    def adjust(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    r, g, b = adjust(r), adjust(g), adjust(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def ensure_contrast(bg_color, text_color=None, min_ratio=7.0):
    """
    Ensure text has sufficient contrast against background
    WCAG AAA standard: 7:1 contrast ratio
    """
    bg_lum = calculate_luminance(bg_color)
    
    if text_color:
        # Check if provided text color has good contrast
        text_lum = calculate_luminance(text_color)
        ratio = (max(bg_lum, text_lum) + 0.05) / (min(bg_lum, text_lum) + 0.05)
        
        if ratio >= min_ratio:
            return text_color
    
    # Generate high-contrast color
    if bg_lum > 0.5:
        # Light background → dark text
        return '#000000'
    else:
        # Dark background → light text
        return '#ffffff'

def parse_color(color_input):
    """Parse color from various formats"""
    if not color_input:
        return None
    
    color_input = color_input.lower().strip()
    
    # Hex color
    if color_input.startswith('#'):
        return color_input
    
    # Named colors to hue
    color_map = {
        'red': 0, 'orange': 30, 'yellow': 60, 'lime': 90,
        'green': 120, 'cyan': 180, 'blue': 240, 'purple': 270,
        'magenta': 300, 'pink': 330, 'white': None, 'black': None
    }
    
    if color_input == 'white':
        return '#ffffff'
    if color_input == 'black':
        return '#000000'
    
    if color_input in color_map:
        hue = color_map[color_input]
        return hsl_to_rgb(hue, 0.8, 0.5)
    
    # RGB format
    if color_input.startswith('rgb'):
        # Basic parsing - production would be more robust
        return color_input
    
    return None

def get_frame_components(frame_id, total_frames=3110400):
    """
    Decompose frame ID into components
    Frame space: 360 hues × 6 bg_styles × 4 geometries × 3 services × 24 times × 5 fonts
    """
    hue = (frame_id * 37) % 360  # Prime number for good distribution
    bg_style_idx = (frame_id // 360) % 6
    geometry_idx = (frame_id // 2160) % 4
    service_idx = (frame_id // 8640) % 3
    time_slot = (frame_id // 25920) % 24
    font_idx = (frame_id // 622080) % 5
    
    return {
        'hue': hue,
        'bg_style': BG_STYLES[bg_style_idx],
        'geometry': GEOMETRY_PATTERNS[geometry_idx],
        'service_idx': service_idx,
        'time_slot': time_slot,
        'font': list(FONT_STYLES.keys())[font_idx]
    }

def calculate_solar_dampener(hour):
    """Calculate brightness based on time of day"""
    normalized = (hour - 6) / 12
    brightness = (math.sin(normalized * math.pi) + 1) / 2
    return max(0.2, min(1.0, brightness))

def create_gradient(hue, bg_style, brightness):
    """Create background gradient based on style"""
    base_color = hsl_to_rgb(hue, 0.7, 0.3 * brightness)
    accent_color = hsl_to_rgb((hue + 30) % 360, 0.6, 0.5 * brightness)
    
    if bg_style == 'vertical':
        return f'<linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{base_color}"/><stop offset="100%" stop-color="{accent_color}"/></linearGradient>'
    elif bg_style == 'horizontal':
        return f'<linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{base_color}"/><stop offset="100%" stop-color="{accent_color}"/></linearGradient>'
    elif bg_style == 'diagonal':
        return f'<linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="{base_color}"/><stop offset="100%" stop-color="{accent_color}"/></linearGradient>'
    elif bg_style == 'radial':
        return f'<radialGradient id="bg"><stop offset="0%" stop-color="{accent_color}"/><stop offset="100%" stop-color="{base_color}"/></radialGradient>'
    elif bg_style == 'double':
        mid_color = hsl_to_rgb((hue + 15) % 360, 0.65, 0.4 * brightness)
        return f'<linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{base_color}"/><stop offset="50%" stop-color="{mid_color}"/><stop offset="100%" stop-color="{accent_color}"/></linearGradient>'
    else:  # triple
        mid1 = hsl_to_rgb((hue + 10) % 360, 0.7, 0.35 * brightness)
        mid2 = hsl_to_rgb((hue + 20) % 360, 0.65, 0.45 * brightness)
        return f'<linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="{base_color}"/><stop offset="33%" stop-color="{mid1}"/><stop offset="66%" stop-color="{mid2}"/><stop offset="100%" stop-color="{accent_color}"/></linearGradient>'

def create_geometry_pattern(geometry, accent_color, index):
    """Create geometric tracer patterns"""
    if geometry == 'sharp':
        return f'''
        <g opacity="0.6">
            <line x1="50" y1="50" x2="150" y2="50" stroke="{accent_color}" stroke-width="2"/>
            <line x1="150" y1="50" x2="150" y2="150" stroke="{accent_color}" stroke-width="2"/>
            <line x1="250" y1="100" x2="350" y2="100" stroke="{accent_color}" stroke-width="2"/>
            <line x1="350" y1="100" x2="350" y2="200" stroke="{accent_color}" stroke-width="2"/>
            <rect x="50" y="350" width="50" height="50" fill="none" stroke="{accent_color}" stroke-width="2"/>
        </g>
        '''
    elif geometry == 'round':
        return f'''
        <g opacity="0.6">
            <circle cx="100" cy="100" r="30" fill="none" stroke="{accent_color}" stroke-width="2"/>
            <circle cx="300" cy="150" r="40" fill="none" stroke="{accent_color}" stroke-width="2"/>
            <path d="M 50 300 Q 100 250 150 300" fill="none" stroke="{accent_color}" stroke-width="2"/>
            <path d="M 250 350 Q 300 300 350 350" fill="none" stroke="{accent_color}" stroke-width="2"/>
        </g>
        '''
    elif geometry == 'minimal':
        return f'''
        <g opacity="0.4">
            <line x1="50" y1="240" x2="350" y2="240" stroke="{accent_color}" stroke-width="1"/>
            <circle cx="200" cy="240" r="100" fill="none" stroke="{accent_color}" stroke-width="1"/>
        </g>
        '''
    else:  # mixed
        pattern = index % 3
        if pattern == 0:
            return f'''
            <g opacity="0.5">
                <path d="M 50 100 L 150 100 L 150 200" stroke="{accent_color}" stroke-width="2" fill="none"/>
                <circle cx="300" cy="150" r="30" fill="none" stroke="{accent_color}" stroke-width="2"/>
                <rect x="250" y="350" width="40" height="40" fill="none" stroke="{accent_color}" stroke-width="2"/>
            </g>
            '''
        elif pattern == 1:
            return f'''
            <g opacity="0.5">
                <line x1="0" y1="0" x2="200" y2="200" stroke="{accent_color}" stroke-width="2"/>
                <circle cx="100" cy="380" r="25" fill="none" stroke="{accent_color}" stroke-width="2"/>
                <path d="M 250 50 Q 300 100 350 50" fill="none" stroke="{accent_color}" stroke-width="2"/>
            </g>
            '''
        else:
            return f'''
            <g opacity="0.5">
                <rect x="50" y="50" width="60" height="60" fill="none" stroke="{accent_color}" stroke-width="2"/>
                <path d="M 250 400 Q 300 350 350 400" fill="none" stroke="{accent_color}" stroke-width="2"/>
                <line x1="200" y1="100" x2="200" y2="180" stroke="{accent_color}" stroke-width="2"/>
            </g>
            '''

def generate_marketing_svg(frame_index, options):
    """
    Generate complete marketing frame
    
    options = {
        'total_frames': int,
        'company': str,
        'services': list,
        'tagline': str or None,
        'url': str or None,
        'bg_color': str or None,
        'text_color': str or None,
        'accent_color': str or None,
        'font': str,
        'geometry': str,
        'contrast': str
    }
    """
    total_frames = options.get('total_frames', 3)
    company = options.get('company', DEFAULT_COMPANY)
    services = options.get('services', DEFAULT_SERVICES)
    tagline = options.get('tagline')
    url = options.get('url')
    font_override = options.get('font')
    geometry_override = options.get('geometry')
    
    # Get frame components
    components = get_frame_components(frame_index)
    
    # Override with user preferences
    if font_override:
        components['font'] = font_override
    if geometry_override:
        components['geometry'] = geometry_override
    
    # Calculate brightness
    brightness = calculate_solar_dampener(components['time_slot'])
    
    # Get colors
    if options.get('bg_color'):
        bg_base = parse_color(options['bg_color']) or hsl_to_rgb(components['hue'], 0.7, 0.3 * brightness)
    else:
        bg_base = hsl_to_rgb(components['hue'], 0.7, 0.3 * brightness)
    
    # Create gradient
    gradient = create_gradient(components['hue'], components['bg_style'], brightness)
    
    # Accent color
    if options.get('accent_color'):
        accent = parse_color(options['accent_color']) or hsl_to_rgb((components['hue'] + 120) % 360, 0.8, 0.6)
    else:
        accent = hsl_to_rgb((components['hue'] + 120) % 360, 0.8, 0.6)
    
    # Text color with contrast enforcement
    if options.get('text_color'):
        text_color_base = parse_color(options['text_color'])
        text_color = ensure_contrast(bg_base, text_color_base)
    else:
        text_color = ensure_contrast(bg_base)
    
    # Get service for this frame
    service_idx = frame_index % len(services)
    service_text = services[service_idx]
    
    # Font style
    font_style = FONT_STYLES[components['font']]
    
    # Geometry pattern
    geometry_svg = create_geometry_pattern(components['geometry'], accent, frame_index)
    
    # Calculate text sizes
    company_size = 36 if len(company) <= 20 else 28
    service_size = 28 if len(service_text) <= 30 else 22
    
    # Build SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 480">
    <defs>
        {gradient}
        <filter id="glow">
            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <filter id="strong-glow">
            <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Background -->
    <rect width="400" height="480" fill="url(#bg)"/>
    
    <!-- Geometry patterns -->
    {geometry_svg}
    
    <!-- Tech corners -->
    <g stroke="{accent}" stroke-width="2" fill="none" opacity="0.7">
        <path d="M 20 20 L 60 20 L 60 60"/>
        <path d="M 380 20 L 340 20 L 340 60"/>
        <path d="M 20 460 L 60 460 L 60 420"/>
        <path d="M 380 460 L 340 460 L 340 420"/>
    </g>
    
    <!-- Company name -->
    <text x="200" y="180" text-anchor="middle" 
          font-family="{font_style['family']}" 
          font-weight="{font_style['weight']}" 
          letter-spacing="{font_style['spacing']}"
          font-size="{company_size}" fill="{text_color}" 
          filter="url(#strong-glow)">
        {company}
    </text>
    
    <!-- Separator line -->
    <line x1="80" y1="200" x2="320" y2="200" stroke="{accent}" stroke-width="2" opacity="{brightness}"/>
    
    <!-- Service -->
    <text x="200" y="250" text-anchor="middle" 
          font-family="{font_style['family']}" 
          font-size="{service_size}" fill="{accent}" 
          filter="url(#glow)">
        {service_text}
    </text>'''
    
    # Add tagline if present
    if tagline:
        svg += f'''
    
    <!-- Tagline -->
    <text x="200" y="300" text-anchor="middle" 
          font-family="Arial" font-size="18" fill="{text_color}" 
          opacity="0.9">
        {tagline}
    </text>'''
    
    # Add URL if present
    if url:
        url_y = 330 if tagline else 300
        svg += f'''
    
    <!-- URL -->
    <text x="200" y="{url_y}" text-anchor="middle" 
          font-family="Arial" font-size="14" fill="{text_color}" 
          opacity="0.8">
        {url}
    </text>'''
    
    # Energy pulse
    svg += f'''
    
    <!-- Energy effects -->
    <circle cx="200" cy="240" r="120" fill="none" 
            stroke="{accent}" stroke-width="1" 
            opacity="{brightness * 0.2}"/>
    <circle cx="200" cy="240" r="140" fill="none" 
            stroke="{accent}" stroke-width="1" 
            opacity="{brightness * 0.1}"/>
    
    <!-- Status dots -->
    <g fill="{accent}" opacity="{brightness}">
        <circle cx="200" cy="360" r="3"/>
        <circle cx="180" cy="360" r="2"/>
        <circle cx="220" cy="360" r="2"/>
    </g>
</svg>'''
    
    return svg
