# myprintfade

**`myprintfade`** is a Python package that provides a simple way to create fading print animations in the terminal. It allows you to display text characters with a fading effect, adding a touch of visual appeal to your command-line applications.

### Installation

You can install `myprintfade` using pip:

```bash
 > pip install myprintfade
```

## Usage

Once installed, you can use the `print_fade` function from the `myprintfade` package in your Python scripts. Here's how to use it:

```python
from myprintfade import print_fade

# Display a fading print animation for "Hello, world!"
print_fade("Hello, world!")
```

The `print_fade` function accepts a message as its argument and displays it with a fading effect.

### Parameters

**`message`** (str): The text message you want to display with a fading effect.
**`delay`** (float, optional): The delay between each character's appearance. Default is 0.05 seconds.
**`fade_steps`** (int, optional): The number of steps in the fade effect. Default is 10.

## Example

```python
from myprintfade import print_fade

# Display a fading print animation for "Python"
print_fade("Python", delay=0.02, fade_steps=8)
```

## Author

>Yassine Naanani
>Email: <prs.online.00@gmail.com>

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on GitHub or submit a pull request.
