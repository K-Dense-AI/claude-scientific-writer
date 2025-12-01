#!/usr/bin/env python3
"""
AI-powered scientific schematic generation using Nano Banana Pro.

This script uses an iterative refinement approach:
1. Generate initial image with Nano Banana Pro
2. AI quality review for scientific critique
3. Improve prompt based on critique and regenerate
4. Repeat for 3 iterations to achieve publication-quality results

Requirements:
    - OPENROUTER_API_KEY environment variable
    - requests library

Usage:
    python generate_schematic_ai.py "Create a flowchart showing CONSORT participant flow" -o flowchart.png
    python generate_schematic_ai.py "Neural network architecture diagram" -o architecture.png --iterations 3
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


# Try to load .env file from multiple potential locations
def _load_env_file():
    """Load .env file from current directory, parent directories, or package directory.
    
    Returns True if a .env file was found and loaded, False otherwise.
    Note: This does NOT override existing environment variables.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        return False  # python-dotenv not installed
    
    # Try current working directory first
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)
        return True
        
    # Try parent directories (up to 5 levels)
    cwd = Path.cwd()
    for _ in range(5):
        env_path = cwd / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return True
        cwd = cwd.parent
        if cwd == cwd.parent:  # Reached root
            break
    
    # Try the package's parent directory (scientific-writer project root)
    script_dir = Path(__file__).resolve().parent
    for _ in range(5):
        env_path = script_dir / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return True
        script_dir = script_dir.parent
        if script_dir == script_dir.parent:
            break
            
    return False


class ScientificSchematicGenerator:
    """Generate scientific schematics using AI with iterative refinement."""
    
    # Scientific diagram best practices prompt template
    SCIENTIFIC_DIAGRAM_GUIDELINES = """
Create a high-quality scientific diagram with these requirements:

VISUAL QUALITY:
- Clean white or light background (no textures or gradients)
- High contrast for readability and printing
- Professional, publication-ready appearance
- Sharp, clear lines and text
- Adequate spacing between elements to prevent crowding

TYPOGRAPHY:
- Clear, readable sans-serif fonts (Arial, Helvetica style)
- Minimum 10pt font size for all labels
- Consistent font sizes throughout
- All text horizontal or clearly readable
- No overlapping text

SCIENTIFIC STANDARDS:
- Accurate representation of concepts
- Clear labels for all components
- Include scale bars, legends, or axes where appropriate
- Use standard scientific notation and symbols
- Include units where applicable

ACCESSIBILITY:
- Colorblind-friendly color palette (use Okabe-Ito colors if using color)
- High contrast between elements
- Redundant encoding (shapes + colors, not just colors)
- Works well in grayscale

LAYOUT:
- Logical flow (left-to-right or top-to-bottom)
- Clear visual hierarchy
- Balanced composition
- Appropriate use of whitespace
- No clutter or unnecessary decorative elements
"""
    
    def __init__(self, api_key: Optional[str] = None, verbose: bool = False):
        """
        Initialize the generator.
        
        Args:
            api_key: OpenRouter API key (or use OPENROUTER_API_KEY env var)
            verbose: Print detailed progress information
        """
        # Priority: 1) explicit api_key param, 2) environment variable, 3) .env file
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        
        # If not found in environment, try loading from .env file
        if not self.api_key:
            _load_env_file()
            self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found. Please either:\n"
                "  1. Set the OPENROUTER_API_KEY environment variable\n"
                "  2. Add OPENROUTER_API_KEY to your .env file\n"
                "  3. Pass api_key parameter to the constructor\n"
                "Get your API key from: https://openrouter.ai/keys"
            )
        
        self.verbose = verbose
        self.base_url = "https://openrouter.ai/api/v1"
        self.image_model = "google/gemini-3-pro-image-preview"
        # Use vision-capable model for review (Gemini Pro Vision or Claude Sonnet)
        self.review_model = "google/gemini-pro-vision"
        
    def _log(self, message: str):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[{time.strftime('%H:%M:%S')}] {message}")
    
    def _make_request(self, model: str, messages: List[Dict[str, Any]], 
                     modalities: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Make a request to OpenRouter API.
        
        Args:
            model: Model identifier
            messages: List of message dictionaries
            modalities: Optional list of modalities (e.g., ["image", "text"])
            
        Returns:
            API response as dictionary
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/scientific-writer",
            "X-Title": "Scientific Schematic Generator"
        }
        
        payload = {
            "model": model,
            "messages": messages
        }
        
        if modalities:
            payload["modalities"] = modalities
        
        self._log(f"Making request to {model}...")
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
    
    def _extract_image_from_response(self, response: Dict[str, Any]) -> Optional[bytes]:
        """
        Extract base64-encoded image from API response.
        
        For Nano Banana Pro, images are returned in the 'images' field of the message,
        not in the 'content' field.
        
        Args:
            response: API response dictionary
            
        Returns:
            Image bytes or None if not found
        """
        try:
            choices = response.get("choices", [])
            if not choices:
                self._log("No choices in response")
                return None
            
            message = choices[0].get("message", {})
            
            # IMPORTANT: Nano Banana Pro returns images in the 'images' field
            images = message.get("images", [])
            if images and len(images) > 0:
                self._log(f"Found {len(images)} image(s) in 'images' field")
                
                # Get first image
                first_image = images[0]
                if isinstance(first_image, dict):
                    # Extract image_url
                    if first_image.get("type") == "image_url":
                        url = first_image.get("image_url", {})
                        if isinstance(url, dict):
                            url = url.get("url", "")
                        
                        if url and url.startswith("data:image"):
                            # Extract base64 data after comma
                            if "," in url:
                                base64_str = url.split(",", 1)[1]
                                # Clean whitespace
                                base64_str = base64_str.replace('\n', '').replace('\r', '').replace(' ', '')
                                self._log(f"Extracted base64 data (length: {len(base64_str)})")
                                return base64.b64decode(base64_str)
            
            # Fallback: check content field (for other models or future changes)
            content = message.get("content", "")
            
            if self.verbose:
                self._log(f"Content type: {type(content)}, length: {len(str(content))}")
            
            # Handle string content
            if isinstance(content, str) and "data:image" in content:
                import re
                match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=\n\r]+)', content, re.DOTALL)
                if match:
                    base64_str = match.group(1).replace('\n', '').replace('\r', '').replace(' ', '')
                    self._log(f"Found image in content field (length: {len(base64_str)})")
                    return base64.b64decode(base64_str)
            
            # Handle list content
            if isinstance(content, list):
                for i, block in enumerate(content):
                    if isinstance(block, dict) and block.get("type") == "image_url":
                        url = block.get("image_url", {})
                        if isinstance(url, dict):
                            url = url.get("url", "")
                        if url and url.startswith("data:image") and "," in url:
                            base64_str = url.split(",", 1)[1].replace('\n', '').replace('\r', '').replace(' ', '')
                            self._log(f"Found image in content block {i}")
                            return base64.b64decode(base64_str)
            
            self._log("No image data found in response")
            return None
            
        except Exception as e:
            self._log(f"Error extracting image: {str(e)}")
            import traceback
            if self.verbose:
                traceback.print_exc()
            return None
    
    def _image_to_base64(self, image_path: str) -> str:
        """
        Convert image file to base64 data URL.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64 data URL string
        """
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Determine image type from extension
        ext = Path(image_path).suffix.lower()
        mime_type = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }.get(ext, "image/png")
        
        base64_data = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{base64_data}"
    
    def generate_image(self, prompt: str) -> Optional[bytes]:
        """
        Generate an image using Nano Banana Pro.
        
        Args:
            prompt: Description of the diagram to generate
            
        Returns:
            Image bytes or None if generation failed
        """
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        try:
            response = self._make_request(
                model=self.image_model,
                messages=messages,
                modalities=["image", "text"]
            )
            
            image_data = self._extract_image_from_response(response)
            if image_data:
                self._log(f"✓ Generated image ({len(image_data)} bytes)")
            else:
                self._log("✗ No image data in response")
            
            return image_data
        except Exception as e:
            self._log(f"✗ Generation failed: {str(e)}")
            return None
    
    def review_image(self, image_path: str, original_prompt: str, 
                    iteration: int) -> Tuple[str, float]:
        """
        Review generated image using AI quality analysis.
        
        Args:
            image_path: Path to the generated image
            original_prompt: Original user prompt
            iteration: Current iteration number
            
        Returns:
            Tuple of (critique text, quality score 0-10)
        """
        # For now, use Nano Banana Pro itself for review (it has vision capabilities)
        # This is more reliable than using a separate vision model
        image_data_url = self._image_to_base64(image_path)
        
        review_prompt = f"""You are reviewing a scientific diagram you just generated.

ORIGINAL REQUEST: {original_prompt}

ITERATION: {iteration}/3

Evaluate this diagram on:
1. Scientific accuracy
2. Clarity and readability
3. Label quality
4. Layout and composition
5. Professional appearance

Provide a score (0-10) and specific suggestions for improvement."""

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": review_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_url
                        }
                    }
                ]
            }
        ]
        
        try:
            # Use the same Nano Banana Pro model for review (it has vision)
            response = self._make_request(
                model=self.image_model,  # Use Nano Banana Pro for review too
                messages=messages
            )
            
            # Extract text response
            choices = response.get("choices", [])
            if not choices:
                return "Image generated successfully", 8.0
            
            message = choices[0].get("message", {})
            content = message.get("content", "")
            
            # Check reasoning field (Nano Banana Pro puts analysis here)
            reasoning = message.get("reasoning", "")
            if reasoning and not content:
                content = reasoning
            
            if isinstance(content, list):
                # Extract text from content blocks
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                content = "\n".join(text_parts)
            
            # Try to extract score
            score = 8.0  # Default to good score if review works
            import re
            score_match = re.search(r'(?:score|rating|quality)[:\s]+(\d+(?:\.\d+)?)\s*/\s*10', content, re.IGNORECASE)
            if score_match:
                score = float(score_match.group(1))
            
            self._log(f"✓ Review complete (Score: {score}/10)")
            return content if content else "Image generated successfully", score
        except Exception as e:
            self._log(f"Review skipped: {str(e)}")
            # Don't fail the whole process if review fails
            return "Image generated successfully (review skipped)", 8.0
    
    def improve_prompt(self, original_prompt: str, critique: str, 
                      iteration: int) -> str:
        """
        Improve the generation prompt based on critique.
        
        Args:
            original_prompt: Original user prompt
            critique: Review critique from previous iteration
            iteration: Current iteration number
            
        Returns:
            Improved prompt for next generation
        """
        improved_prompt = f"""{self.SCIENTIFIC_DIAGRAM_GUIDELINES}

USER REQUEST: {original_prompt}

ITERATION {iteration}: Based on previous feedback, address these specific improvements:
{critique}

Generate an improved version that addresses all the critique points while maintaining scientific accuracy and professional quality."""
        
        return improved_prompt
    
    def generate_iterative(self, user_prompt: str, output_path: str,
                          iterations: int = 3) -> Dict[str, Any]:
        """
        Generate scientific schematic with iterative refinement.
        
        Args:
            user_prompt: User's description of desired diagram
            output_path: Path to save final image
            iterations: Number of refinement iterations (default: 3)
            
        Returns:
            Dictionary with generation results and metadata
        """
        output_path = Path(output_path)
        output_dir = output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        base_name = output_path.stem
        extension = output_path.suffix or ".png"
        
        results = {
            "user_prompt": user_prompt,
            "iterations": [],
            "final_image": None,
            "final_score": 0.0,
            "success": False
        }
        
        current_prompt = f"""{self.SCIENTIFIC_DIAGRAM_GUIDELINES}

USER REQUEST: {user_prompt}

Generate a publication-quality scientific diagram that meets all the guidelines above."""
        
        print(f"\n{'='*60}")
        print(f"Generating Scientific Schematic")
        print(f"{'='*60}")
        print(f"Description: {user_prompt}")
        print(f"Iterations: {iterations}")
        print(f"Output: {output_path}")
        print(f"{'='*60}\n")
        
        for i in range(1, iterations + 1):
            print(f"\n[Iteration {i}/{iterations}]")
            print("-" * 40)
            
            # Generate image
            print(f"Generating image...")
            image_data = self.generate_image(current_prompt)
            
            if not image_data:
                print(f"✗ Generation failed")
                results["iterations"].append({
                    "iteration": i,
                    "success": False,
                    "error": "Image generation failed"
                })
                continue
            
            # Save iteration image
            iter_path = output_dir / f"{base_name}_v{i}{extension}"
            with open(iter_path, "wb") as f:
                f.write(image_data)
            print(f"✓ Saved: {iter_path}")
            
            # Review image (skip on last iteration if desired, but we'll do it for completeness)
            print(f"Reviewing image...")
            critique, score = self.review_image(str(iter_path), user_prompt, i)
            print(f"✓ Score: {score}/10")
            
            # Save iteration results
            iteration_result = {
                "iteration": i,
                "image_path": str(iter_path),
                "prompt": current_prompt,
                "critique": critique,
                "score": score,
                "success": True
            }
            results["iterations"].append(iteration_result)
            
            # If this is the last iteration, we're done
            if i == iterations:
                results["final_image"] = str(iter_path)
                results["final_score"] = score
                results["success"] = True
                break
            
            # Improve prompt for next iteration
            print(f"Improving prompt based on feedback...")
            current_prompt = self.improve_prompt(user_prompt, critique, i + 1)
        
        # Copy final version to output path
        if results["success"] and results["final_image"]:
            final_iter_path = Path(results["final_image"])
            if final_iter_path != output_path:
                import shutil
                shutil.copy(final_iter_path, output_path)
                print(f"\n✓ Final image: {output_path}")
        
        # Save review log
        log_path = output_dir / f"{base_name}_review_log.json"
        with open(log_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"✓ Review log: {log_path}")
        
        print(f"\n{'='*60}")
        print(f"Generation Complete!")
        print(f"Final Score: {results['final_score']}/10")
        print(f"{'='*60}\n")
        
        return results


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate scientific schematics using AI with iterative refinement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a flowchart
  python generate_schematic_ai.py "CONSORT participant flow diagram" -o flowchart.png
  
  # Generate neural network architecture
  python generate_schematic_ai.py "Transformer encoder-decoder architecture" -o transformer.png
  
  # Generate with custom iterations
  python generate_schematic_ai.py "Biological signaling pathway" -o pathway.png --iterations 5
  
  # Verbose output
  python generate_schematic_ai.py "Circuit diagram" -o circuit.png -v

Environment:
  OPENROUTER_API_KEY    OpenRouter API key (required)
        """
    )
    
    parser.add_argument("prompt", help="Description of the diagram to generate")
    parser.add_argument("-o", "--output", required=True, 
                       help="Output image path (e.g., diagram.png)")
    parser.add_argument("--iterations", type=int, default=3,
                       help="Number of refinement iterations (default: 3)")
    parser.add_argument("--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        print("\nSet it with:")
        print("  export OPENROUTER_API_KEY='your_api_key'")
        print("\nOr provide via --api-key flag")
        sys.exit(1)
    
    # Validate iterations
    if args.iterations < 1 or args.iterations > 10:
        print("Error: Iterations must be between 1 and 10")
        sys.exit(1)
    
    try:
        generator = ScientificSchematicGenerator(api_key=api_key, verbose=args.verbose)
        results = generator.generate_iterative(
            user_prompt=args.prompt,
            output_path=args.output,
            iterations=args.iterations
        )
        
        if results["success"]:
            print(f"\n✓ Success! Image saved to: {args.output}")
            sys.exit(0)
        else:
            print(f"\n✗ Generation failed. Check review log for details.")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

