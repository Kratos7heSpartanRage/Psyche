import streamlit as st

def render_matrix_rain():
    """Render the Matrix rain effect using components.v1.html"""
    matrix_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body, html {
                margin: 0;
                padding: 0;
                overflow: hidden;
                width: 100%;
                height: 100%;
                position: fixed;
                top: 0;
                left: 0;
            }
            #matrix {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                z-index: -1;
                background: #050709;
            }
            .matrix-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                z-index: 9998;
                background: repeating-linear-gradient(transparent, transparent 1px, rgba(0,0,0,0.15) 2px);
                pointer-events: none;
            }
            
            /* Break out of the iframe */
            iframe {
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                border: none !important;
                z-index: -2 !important;
            }
        </style>
    </head>
    <body>
        <canvas id="matrix"></canvas>
        <div class="matrix-overlay"></div>
        
        <script>
        (function(){
            const canvas = document.getElementById('matrix');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            
            // Set canvas to full screen
            function resize(){
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }
            
            // Initial resize and listen for changes
            resize();
            window.addEventListener('resize', resize);
            
            const fontSize = 16;
            const chars = 'アイウエオカキクケコサシスセソ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
            let columns = Math.floor(canvas.width / fontSize);
            let drops = Array(columns).fill(1);
            
            // Slower animation speed
            let frameCount = 0;
            const framesPerDrop = 3;

            function draw(){
                frameCount++;
                
                // Semi-transparent black to create trail effect
                ctx.fillStyle = 'rgba(5, 7, 9, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                if (frameCount % framesPerDrop === 0) {
                    for(let i = 0; i < drops.length; i++){
                        const charIndex = Math.floor(Math.random() * chars.length);
                        const text = chars[charIndex];
                        const x = i * fontSize;
                        const y = drops[i] * fontSize;
                        
                        // Fading effect - brighter at the head
                        const brightness = 1 - (drops[i] * 0.02);
                        ctx.fillStyle = `rgba(39, 255, 184, ${Math.max(0.2, brightness)})`;
                        ctx.font = `${fontSize}px 'JetBrains Mono', 'Fira Code', monospace`;
                        
                        ctx.fillText(text, x, y);
                        
                        // Reset drop when it reaches bottom with some randomness
                        if (y > canvas.height && Math.random() > 0.98) {
                            drops[i] = 0;
                        }
                        drops[i]++;
                    }
                }
                
                requestAnimationFrame(draw);
            }
            
            draw();

        })();
        </script>
    </body>
    </html>
    """
    
    # Use components to render HTML with JavaScript execution
    # Set height to 0 and use scrolling=False to minimize iframe constraints
    st.components.v1.html(matrix_html, height=0, scrolling=False)

# Keep the original constant for backward compatibility
MATRIX_CANVAS = """
<div style="position: fixed; inset: 0; z-index: -1; background: #050709; pointer-events: none;"></div>
"""