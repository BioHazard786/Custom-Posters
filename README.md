[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Custom Posters</h3>

  <p align="center">
    A api to generate custom anime, tv and movie posters.
    <br />
    <br />
    <a href="https://custom-posters.vercel.app/">View Demo</a>
    ·
    <a href="https://github.com/BioHazard786/Custom-Posters/issues">Report Bug</a>
    ·
    <a href="https://github.com/BioHazard786/Custom-Posters/issues">Request Feature</a>
  </p>
</div>

## Deploy To Vercel

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/BiioHazard786/Custom-Posters)

In production build command is - `gunicorn -w 4 -b 0.0.0.0:8000 app:app`

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Run Locally](#installation)
- [Built With](#built-with)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Getting Started

### Prerequisites

#### Required Variables

- `TMDB_API_KEY`: Get it from [TMDB](https://developer.themoviedb.org/docs/getting-started)

#### Required Softwares

- `Python`: Get this from [python.org](https://www.python.org/downloads/)

### Run Locally

#### 1. Clone Repo

```bash
git clone https://github.com/BioHazard786/Custom-Posters.git custom-poster/
```

#### 2. Setting up config.env file

- Create config.env file in root folder with the following [variables](#required-variables).

#### 2. Running Locally

```bash
# cd into folder
cd custom-poster

# Install dependencies
pip install -r requirements.txt

# uncomment the last line in app.py
# Run Locally
python app.py
```

## Built With

- [Python](https://python.org/) - The main language

- [Pillow](https://pillow.readthedocs.io/en/stable/index.html) - The image manipulation library used

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Mohd Zaid - [@LuLu786](https://t.me/LuLu786) - bzatch70@gmail.com

Project Link : [https://github.com/BioHazard786/Custom-Posters](https://github.com/BioHazard786/Custom-Posters)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/BioHazard786/Custom-Posters.svg?style=for-the-badge
[contributors-url]: https://github.com/BioHazard786/Custom-Posters/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/BioHazard786/Custom-Posters.svg?style=for-the-badge
[forks-url]: https://github.com/BioHazard786/Custom-Posters/network/members
[stars-shield]: https://img.shields.io/github/stars/BioHazard786/Custom-Posters.svg?style=for-the-badge
[stars-url]: https://github.com/BioHazard786/Custom-Posters/stargazers
[issues-shield]: https://img.shields.io/github/issues/BioHazard786/Custom-Posters.svg?style=for-the-badge
[issues-url]: https://github.com/BioHazard786/Custom-Posters/issues
[license-shield]: https://img.shields.io/github/license/BioHazard786/Custom-Posters.svg?style=for-the-badge
[license-url]: https://github.com/BioHazard786/Custom-Posters/blob/master/LICENSE
