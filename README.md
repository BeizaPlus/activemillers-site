# Active™ - React Website

A modern React recreation of the activemillers.com website built with Vite, TypeScript, and Tailwind CSS.

## Features

- **Responsive Design**: Optimized for desktop and mobile devices
- **Modern Stack**: React 19, TypeScript, Vite, Tailwind CSS
- **Email Integration**: GoDaddy email marketing form integration
- **Ken Burns Effect**: Animated background images
- **Social Media**: Instagram and WhatsApp integration
- **Performance**: Fast loading with Vite and optimized assets

## Tech Stack

- **Frontend**: React 19 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS 4
- **Package Manager**: Bun
- **Fonts**: Montserrat, Noto Sans, Roboto

## Getting Started

### Prerequisites

- [Bun](https://bun.sh/) installed on your system

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd activemillers-react
```

2. Install dependencies:

```bash
bun install
```

3. Start the development server:

```bash
bun dev
```

4. Open your browser and navigate to `http://localhost:5173`

## Project Structure

```
src/
├── components/
│   ├── ActiveLogo.tsx          # SVG logo component
│   ├── EmailSignupForm.tsx     # Email subscription form
│   ├── HeroSection.tsx         # Desktop hero section
│   ├── MobileHeroSection.tsx   # Mobile hero section
│   └── SocialSection.tsx       # Social media links
├── App.tsx                     # Main app component
├── main.tsx                    # App entry point
└── index.css                   # Global styles and Tailwind imports
```

## Key Components

### HeroSection

- Full-screen background with Ken Burns animation
- Active logo display
- Email signup form
- Call-to-action buttons

### MobileHeroSection

- Mobile-optimized layout
- Scaled logo and content
- Simplified navigation

### EmailSignupForm

- GoDaddy email marketing integration
- Form validation
- Honeypot spam protection
- Success/error messaging

### ActiveLogo

- SVG logo component
- Scalable and customizable
- Matches original design

## Customization

### Colors

The color scheme is defined in `tailwind.config.js`:

- Primary Red: `#e60021`
- Active Black: `#231916`

### Fonts

Custom fonts are loaded from Google Fonts:

- Montserrat (headings)
- Noto Sans (body text)
- Roboto (buttons)

### Background Images

Replace the background images in the hero sections with your own:

- Desktop: Update the `backgroundImage` style in `HeroSection.tsx`
- Mobile: Update the `backgroundImage` style in `MobileHeroSection.tsx`

## Deployment

### Build for Production

```bash
bun run build
```

### Preview Production Build

```bash
bun run preview
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is a recreation of the activemillers.com website for educational purposes.
