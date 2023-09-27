from setuptools import setup

setup(
    name='myprintfade',
    version='0.2',
    description='Create Stunning Text Animations While Printing in Python',
    long_description='''
    MyPrintFade is a Python package that empowers developers to elevate their console text output with captivating animations. It offers a simple yet powerful way to create eye-catching text effects during printing, enhancing user experience in terminal applications.

    Key Features:
    - Slide Text Animation: Slide your text smoothly from left to right, adding a dynamic touch to your messages.
    - Fade-In Effect: Gradually fade in your text, creating a subtle and elegant introduction.
    - Customizable Delays: Fine-tune animation speed to match your application's requirements.
    - Easy to Use: A straightforward API allows you to integrate stunning animations with just a few lines of code.

    Usage:
    Getting started is easy. Import the 'myprintfade' module and use it to print text with animated effects:

    ```python
    from myprintfade import print_slide, print_fade

    message = "Hello, Python!"
    
    # Slide text animation
    print_slide(message, delay=0.1)
    
    # Fade-in effect
    print_fade(message, delay=0.05)
    ```

    Elevate your command-line applications by transforming ordinary text into engaging visual experiences with MyPrintFade.

    Explore the documentation for more details and customization options.

    Installation:
    ```
    pip install myprintfade
    ```

    GitHub Repository: https://github.com/K11E3R/myprintfade

    License: MIT License

    Questions or Feedback? Feel free to contact us at prs.online.00@gmail.com.

    Enjoy creating stunning text animations in Python with MyPrintFade!
    ''',
)
