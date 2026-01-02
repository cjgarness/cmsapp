# Modern Template System - AltusPath CMS

## Overview

The modern template system provides responsive, mobile-first HTML templates with a nature-inspired color scheme for the AltusPath CMS. These templates are designed to work seamlessly with both desktop and mobile devices.

## Design Features

### Color Scheme (Nature-Inspired Bold Colors)

| Color Name | Hex Value | Usage |
|-----------|-----------|-------|
| **Forest Green** | #1b4d3e | Primary headings, borders, accents |
| **Forest Green Light** | #2d5016 | Alternative backgrounds |
| **Ocean Blue** | #0066cc | Links, buttons, primary CTA |
| **Ocean Blue Light** | #4a90e2 | Hover states, lighter elements |
| **Earth Brown** | #8b6f47 | Secondary accents |
| **Terracotta** | #d97e6e | Alert/warning elements |
| **Sky Blue** | #87ceeb | Background overlays, subtle accents |

### Layout Features

- **Responsive Design**: Mobile-first approach that adapts to all screen sizes
- **Sticky Navigation**: Easy access to site navigation on scroll
- **Hero Sections**: Eye-catching header areas with optional background images
- **Card Layouts**: Grid-based page/content displays with smooth hover effects
- **Semantic HTML**: Proper heading hierarchy and accessibility
- **CSS Custom Properties**: Easy theming and customization
- **Intersection Observer**: Smooth fade-in animations on scroll

## Templates

### 1. **modern/base.html**
Base template extending Django's template system. All other templates inherit from this.

**Includes:**
- Sticky navigation bar with hamburger menu for mobile
- Footer with contact info and quick links
- JavaScript for menu interactions
- Meta tags and CSS loading

**Context Variables:**
- `navbar_pages`: Optional list of pages to show in navigation

### 2. **modern/page_detail.html**
Displays individual page content with full formatting support.

**Features:**
- Hero section with featured image (optional)
- Page title and description
- Rich content area with HTML support
- Page blocks (content sections)
- Image gallery with lazy loading
- Publication metadata
- Responsive image grid

**Context Variables:**
- `page`: Page object with title, description, content, featured_image
- `blocks`: List of PageBlock objects
- `images`: List of PageImage objects

### 3. **modern/page_list.html**
Displays a grid of pages with cards and pagination.

**Features:**
- Responsive grid layout (1-3 columns depending on screen size)
- Page cards with image, title, description
- Placeholder for pages without featured images
- Read More links
- Pagination controls
- Empty state message

**Context Variables:**
- `pages`: List of Page objects
- `is_paginated`: Boolean for pagination
- `page_obj`: Pagination object

### 4. **modern/homepage.html**
Landing page template with hero and featured sections.

**Features:**
- Full-width hero section with animated background shapes
- CTA buttons (Explore Pages, Contact Us)
- Homepage blocks for custom content sections
- Call-to-action section
- Animated background elements

**Context Variables:**
- `blocks`: List of homepage PageBlock objects

### 5. **modern/contact.html**
Contact form template with form fields and contact info.

**Features:**
- Contact form with validation
- Responsive two-column layout
- Contact information blocks with icons
- Email, phone, and hours display
- Error handling and success messaging
- Mobile-responsive layout

**Context Variables:**
- `form`: Contact form instance
- Contact information hardcoded (customize as needed)

## CSS Files

### **static/css/modern-base.css**
Main stylesheet containing:
- CSS custom properties (variables) for colors and spacing
- Base element styles
- Component-specific styling
- Responsive breakpoints (768px, 480px)
- Mobile-first approach
- Smooth transitions and animations

**Key Sections:**
- Navigation styles
- Hero sections
- Cards and grids
- Buttons and forms
- Footer
- Responsive utilities

## JavaScript Files

### **static/js/modern-nav.js**
Interactive navigation features:
- Hamburger menu toggle
- Mobile menu opening/closing
- Smooth scrolling for anchor links
- Active link highlighting
- Intersection Observer for fade-in animations

## Setup Instructions

### 1. Create the Domain (if needed)

```bash
python manage.py shell
```

```python
from cmsapp.domains.models import Domain

domain = Domain.objects.create(
    name='altuspath.com',
    title='AltusPath',
    is_active=True
)
```

### 2. Set Up Modern Templates

```bash
python manage.py setup_modern_templates --domain altuspath.com
```

This creates the following PageTemplate records:
- Modern Base
- Modern Page Detail (default)
- Modern Page List
- Modern Homepage

### 3. Apply Modern Stylesheet

```bash
python manage.py apply_modern_stylesheet --domain altuspath.com
```

This creates a Stylesheet record for domain-specific overrides.

### 4. Create Sample Pages

```bash
python manage.py shell
```

```python
from cmsapp.pages.models import Page
from cmsapp.domains.models import Domain

domain = Domain.objects.get(name='altuspath.com')

# Homepage
homepage = Page.objects.create(
    domain=domain,
    title='Welcome to AltusPath',
    slug='home',
    description='Building modern web experiences with nature-inspired design',
    content='<h2>Your homepage content goes here</h2><p>Edit this in the admin.</p>',
    is_published=True,
)

# About page
about = Page.objects.create(
    domain=domain,
    title='About AltusPath',
    slug='about',
    description='Learn about our mission and values',
    content='<p>Write your about page content here.</p>',
    is_published=True,
)
```

## Customization Guide

### Colors

Edit the CSS custom properties in `static/css/modern-base.css`:

```css
:root {
    --color-forest: #1b4d3e;
    --color-ocean: #0066cc;
    /* etc. */
}
```

### Spacing

Adjust spacing scale:

```css
:root {
    --spacing-xs: 0.5rem;
    --spacing-sm: 1rem;
    --spacing-md: 2rem;
    --spacing-lg: 3rem;
    --spacing-xl: 4rem;
}
```

### Responsive Breakpoints

Mobile breakpoints are at 768px and 480px. Adjust in CSS media queries:

```css
@media (max-width: 768px) {
    /* tablet/small desktop adjustments */
}

@media (max-width: 480px) {
    /* mobile adjustments */
}
```

### Logo/Branding

Edit [modern/base.html](modern/base.html):

```html
<a href="{% url 'pages:homepage' %}" class="nav-logo">
    <span class="logo-text">Your Brand Here</span>
</a>
```

Or add an image:

```html
<a href="{% url 'pages:homepage' %}" class="nav-logo">
    <img src="{% static 'img/logo.png' %}" alt="Logo">
</a>
```

### Footer Content

Edit [modern/base.html](modern/base.html) footer section:

```html
<div class="footer-section">
    <h4>Company Name</h4>
    <p>Your company description</p>
</div>
```

### Navigation Items

Add menu items in [modern/base.html](modern/base.html):

```html
<ul class="nav-menu" id="navMenu">
    <li><a href="{% url 'pages:homepage' %}" class="nav-link">Home</a></li>
    <li><a href="{% url 'pages:page_list' %}" class="nav-link">Pages</a></li>
    <li><a href="/custom-url/" class="nav-link">Custom Page</a></li>
    <li><a href="{% url 'contact:contact' %}" class="nav-link nav-link-primary">Contact</a></li>
</ul>
```

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Full support
- IE 11: Not supported

## Accessibility Features

- Semantic HTML structure
- Proper heading hierarchy
- Alt text for images
- Color contrast meets WCAG standards
- Keyboard navigation support
- Focus indicators for interactive elements
- Lazy loading for images

## Performance Optimizations

- CSS variables for efficient theming
- Minimal JavaScript (vanilla JS, no jQuery)
- Image lazy loading with `loading="lazy"`
- Optimized CSS file (one main stylesheet)
- Smooth transitions using CSS (not JS)
- Intersection Observer for animations

## Mobile Viewport

All templates include proper viewport meta tag:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

Mobile menu transforms to hamburger at 768px breakpoint.

## Contact Form Customization

Edit [modern/contact.html](modern/contact.html) contact info:

```html
<p><a href="mailto:your-email@example.com">your-email@example.com</a></p>
<p><a href="tel:+1234567890">(123) 456-7890</a></p>
<p>Mon - Fri: 9am - 5pm CST</p>
```

## Admin Integration

The templates work with the standard Django admin:

1. Create pages in `/admin/pages/page/`
2. Assign pages to the modern template
3. Add page blocks and images
4. Publish when ready

## Troubleshooting

### Templates Not Loading
- Ensure templates folder is in TEMPLATES setting
- Check `DEBUG=True` in development
- Verify STATIC_URL and STATIC_ROOT settings

### Styles Not Loading
- Clear browser cache (Ctrl+Shift+Delete)
- Run `python manage.py collectstatic`
- Check STATIC_ROOT permissions
- Verify CSS file exists at path

### Mobile Menu Not Working
- Check JavaScript console for errors
- Verify `modern-nav.js` is loaded
- Check hamburger element ID is `hamburger`

### Images Not Displaying
- Verify MEDIA_URL and MEDIA_ROOT settings
- Check image file permissions
- Try clearing media cache

## File Structure

```
templates/
├── modern/
│   ├── base.html
│   ├── page_detail.html
│   ├── page_list.html
│   ├── homepage.html
│   └── contact.html

static/
├── css/
│   └── modern-base.css
└── js/
    └── modern-nav.js
```

## Future Enhancements

- Dark mode toggle
- Additional color themes
- Animation customization
- Font family options
- Layout variant templates
- Search functionality
- Social media integration

## Support

For issues or customization assistance, refer to:
- MULTI_DOMAIN_GUIDE.md (for domain setup)
- Django template documentation
- CMS admin panel help text
