#!/usr/bin/env python3
"""
Dynamic Marketing GIF Server
Complete marketing GIF generation with full customization
"""

from flask import Flask, Response, request
from flask_cors import CORS
import os
import random
import urllib.parse
from io import BytesIO

try:
    import cairosvg
    HAS_CAIRO = True
except ImportError:
    HAS_CAIRO = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from generate_marketing import generate_marketing_svg, DEFAULT_COMPANY, DEFAULT_SERVICES

app = Flask(__name__)
CORS(app)

def parse_services(services_param):
    """Parse comma-separated services list"""
    if not services_param:
        return DEFAULT_SERVICES
    
    services = [s.strip() for s in services_param.split(',')]
    services = [urllib.parse.unquote(s) for s in services if s]
    
    return services[:10]  # Max 10 services

def get_frame_indices(count, random_mode, seed=None):
    """Get frame indices based on mode"""
    if random_mode:
        if seed:
            random.seed(seed)
        return random.sample(range(3110400), min(count, 3110400))
    else:
        return list(range(count))

@app.route('/')
def index():
    """Landing page with documentation"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dynamic Marketing GIF Generator</title>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                max-width: 1000px;
                margin: 40px auto;
                padding: 30px;
                background: linear-gradient(135deg, #0a0520 0%, #1a4d7a 100%);
                color: #ffffff;
            }
            .container {
                background: rgba(255, 255, 255, 0.05);
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
                border: 1px solid rgba(0, 255, 255, 0.2);
            }
            h1 {
                color: #00ffff;
                text-shadow: 0 0 20px #00ffff;
                font-size: 2.8em;
                margin-bottom: 10px;
            }
            h2 {
                color: #ff00ff;
                border-bottom: 2px solid #ff00ff;
                padding-bottom: 10px;
                margin-top: 40px;
            }
            code {
                background: rgba(0, 0, 0, 0.5);
                padding: 3px 10px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                color: #00ff00;
                border: 1px solid #00ff00;
                font-size: 0.95em;
            }
            .example {
                margin: 20px 0;
                padding: 20px;
                background: rgba(0, 100, 200, 0.1);
                border-left: 4px solid #00ffff;
                border-radius: 4px;
            }
            .gif-demo {
                text-align: center;
                margin: 30px 0;
                padding: 25px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
            }
            img {
                border: 3px solid #00ffff;
                margin: 15px;
                box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border: 1px solid rgba(0, 255, 255, 0.3);
            }
            th {
                background: rgba(0, 255, 255, 0.2);
                color: #00ffff;
            }
            .param {
                color: #ffaa00;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ Dynamic Marketing GIF</h1>
            <p style="font-size: 1.3em; color: #ffaa00;">Complete marketing automation with 3.1 million unique combinations</p>
            
            <h2>🎯 Quick Start</h2>
            <div class="example">
                <code>/marketing.gif?count=3</code>
                <p style="margin-top: 10px;">Generate a 3-frame animated GIF</p>
            </div>
            
            <h2>🎬 Live Examples</h2>
            
            <div class="gif-demo">
                <h3>Simple (3 frames)</h3>
                <img src="/marketing.gif?count=3" width="200">
                <p><code>/marketing.gif?count=3</code></p>
            </div>
            
            <div class="gif-demo">
                <h3>Custom Company</h3>
                <img src="/marketing.gif?count=3&company=TechCorp&services=Web,Mobile,Cloud" width="200">
                <p><code>/marketing.gif?count=3&company=TechCorp&services=Web,Mobile,Cloud</code></p>
            </div>
            
            <h2>📋 Complete API</h2>
            
            <h3>Frame Control</h3>
            <table>
                <tr><th>Parameter</th><th>Values</th><th>Description</th></tr>
                <tr><td class="param">count</td><td>1-100, 0</td><td>Number of frames (0 = surprise mode)</td></tr>
                <tr><td class="param">random</td><td>true/false</td><td>Random sampling from 3.1M space</td></tr>
                <tr><td class="param">frame</td><td>0-3110399</td><td>Specific frame ID(s), comma-separated</td></tr>
                <tr><td class="param">seed</td><td>text</td><td>Seed for reproducible random</td></tr>
                <tr><td class="param">duration</td><td>milliseconds</td><td>Frame duration (default: 1000)</td></tr>
            </table>
            
            <h3>Text Control</h3>
            <table>
                <tr><th>Parameter</th><th>Example</th><th>Description</th></tr>
                <tr><td class="param">company</td><td>YourBrand</td><td>Company/brand name</td></tr>
                <tr><td class="param">services</td><td>A,B,C</td><td>Comma-separated services list</td></tr>
                <tr><td class="param">tagline</td><td>Your Slogan</td><td>Optional tagline text</td></tr>
                <tr><td class="param">url</td><td>yourbrand.com</td><td>Optional website URL</td></tr>
            </table>
            
            <h3>Visual Control</h3>
            <table>
                <tr><th>Parameter</th><th>Values</th><th>Description</th></tr>
                <tr><td class="param">bg</td><td>blue, red, #FF0000</td><td>Background color</td></tr>
                <tr><td class="param">text</td><td>white, cyan, #00FFFF</td><td>Text color (auto-contrast)</td></tr>
                <tr><td class="param">accent</td><td>yellow, purple</td><td>Accent color</td></tr>
                <tr><td class="param">font</td><td>bold, tech, elegant, blocky, script</td><td>Font style</td></tr>
                <tr><td class="param">geometry</td><td>sharp, round, mixed, minimal</td><td>Geometric style</td></tr>
            </table>
            
            <h2>💡 Usage Examples</h2>
            
            <div class="example">
                <h4>Restaurant Menu</h4>
                <code>/marketing.gif?count=5&company=Joe's Diner&services=Breakfast,Lunch,Dinner,Desserts,Drinks</code>
            </div>
            
            <div class="example">
                <h4>Tech Startup</h4>
                <code>/marketing.gif?count=3&company=StartupXYZ&services=Platform,API,Consulting&font=tech&geometry=sharp</code>
            </div>
            
            <div class="example">
                <h4>Random Fresh Content</h4>
                <code>/marketing.gif?count=10&random=true&company=YourBrand&services=Product1,Product2,Product3</code>
            </div>
            
            <div class="example">
                <h4>Color Themed</h4>
                <code>/marketing.gif?count=6&bg=blue&text=white&accent=red&company=USA Brand</code>
            </div>
            
            <div class="example">
                <h4>Surprise Me!</h4>
                <code>/marketing.gif?count=0&company=YourBrand</code>
            </div>
            
            <h2>✨ Features</h2>
            <ul style="line-height: 2;">
                <li><strong>3.1 Million Combinations:</strong> 360 hues × 6 gradients × 4 geometries × 24 times × 5 fonts</li>
                <li><strong>Automatic Contrast:</strong> Text always readable (WCAG AAA)</li>
                <li><strong>Random Mode:</strong> Fresh content every generation</li>
                <li><strong>Frame Access:</strong> Reproducible specific frames</li>
                <li><strong>Solar Dampener:</strong> Time-aware brightness</li>
                <li><strong>Full Customization:</strong> Colors, fonts, geometry, text</li>
                <li><strong>Universal Format:</strong> GIF works everywhere</li>
            </ul>
            
            <h2>🚀 Workflow</h2>
            <ol style="line-height: 2;">
                <li>Build your URL with desired parameters</li>
                <li>Open in browser to preview</li>
                <li>Right-click → Save As → Download GIF</li>
                <li>Upload anywhere (social, email, websites)</li>
                <li>Done in seconds, not hours</li>
            </ol>
            
            <p style="margin-top: 40px; text-align: center; color: #00ffff; font-size: 1.2em;">
                <strong>Dynamic Marketing GIF</strong> | Infinite Possibilities ⚡
            </p>
        </div>
    </body>
    </html>
    '''

@app.route('/marketing.gif')
def serve_marketing_gif():
    """Generate and serve marketing GIF"""
    
    if not HAS_CAIRO or not HAS_PIL:
        return Response(
            "Error: Required libraries missing. Install: pip install cairosvg pillow",
            status=500,
            mimetype='text/plain'
        )
    
    try:
        # Parse parameters
        count_param = request.args.get('count', '3')
        random_mode = request.args.get('random', 'false').lower() == 'true'
        frame_param = request.args.get('frame')
        seed_param = request.args.get('seed')
        duration = int(request.args.get('duration', 1000))
        
        # Text parameters
        company = request.args.get('company', DEFAULT_COMPANY)
        services_param = request.args.get('services')
        services = parse_services(services_param)
        tagline = request.args.get('tagline')
        url = request.args.get('url')
        
        # Visual parameters
        bg_color = request.args.get('bg')
        text_color = request.args.get('text')
        accent_color = request.args.get('accent')
        font = request.args.get('font', 'bold')
        geometry = request.args.get('geometry', 'mixed')
        
        # Determine frame indices
        if frame_param:
            # Specific frame(s)
            if ',' in frame_param:
                frame_indices = [int(f.strip()) for f in frame_param.split(',')]
            else:
                frame_indices = [int(frame_param)]
        else:
            # Count-based
            if count_param == '0':
                # Surprise mode
                count = random.randint(10, 30)
                random_mode = True
                duration = random.randint(500, 1500)
            else:
                count = int(count_param)
            
            if count < 1 or count > 100:
                return Response(
                    "Error: 'count' must be between 1-100 (or 0 for surprise mode)",
                    status=400,
                    mimetype='text/plain'
                )
            
            frame_indices = get_frame_indices(count, random_mode, seed_param)
        
        # Build options dict
        options = {
            'total_frames': len(frame_indices),
            'company': company[:50],  # Limit length
            'services': services,
            'tagline': tagline[:100] if tagline else None,
            'url': url.replace('http://', '').replace('https://', '')[:50] if url else None,
            'bg_color': bg_color,
            'text_color': text_color,
            'accent_color': accent_color,
            'font': font if font in ['bold', 'tech', 'elegant', 'blocky', 'script'] else 'bold',
            'geometry': geometry if geometry in ['sharp', 'round', 'mixed', 'minimal'] else 'mixed',
            'contrast': 'auto'
        }
        
        # Generate frames
        frames = []
        for frame_id in frame_indices:
            svg_content = generate_marketing_svg(frame_id, options)
            png_data = cairosvg.svg2png(
                bytestring=svg_content.encode('utf-8'),
                output_width=400,
                output_height=480
            )
            img = Image.open(BytesIO(png_data))
            frames.append(img)
        
        # Create GIF
        output = BytesIO()
        frames[0].save(
            output,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            optimize=True
        )
        output.seek(0)
        
        return Response(output.read(), mimetype='image/gif')
        
    except ValueError as e:
        return Response(
            f"Error: Invalid parameter value - {str(e)}",
            status=400,
            mimetype='text/plain'
        )
    except Exception as e:
        return Response(
            f"Error generating GIF: {str(e)}",
            status=500,
            mimetype='text/plain'
        )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("⚡ Dynamic Marketing GIF Generator Starting...")
    print(f"📍 Server running on port: {port}")
    print(f"🎨 Frame space: 3,110,400 unique combinations")
    app.run(host='0.0.0.0', port=port, debug=False)
