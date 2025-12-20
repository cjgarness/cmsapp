# Contributing Guide

Thank you for considering contributing to Django CMS! Here's how you can help.

## Code of Conduct

Be respectful and professional in all interactions.

## Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit with descriptive messages (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Development Setup

```bash
./build-dev.sh  # Linux/Mac
build-dev.bat   # Windows
```

## Testing

```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py test
```

## Code Style

- Follow PEP 8 guidelines
- Use 4 spaces for indentation
- Write descriptive commit messages
- Include docstrings for functions

## Adding Features

1. Create a new branch for your feature
2. Write tests for your code
3. Update documentation
4. Submit a Pull Request with a clear description

## Reporting Issues

Please include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Docker version, etc.)

## License

By contributing, you agree your code will be licensed under the MIT License.
