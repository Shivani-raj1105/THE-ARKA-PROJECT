---
name: Organic Botanist
colors:
  surface: '#f9faf6'
  surface-dim: '#d9dad7'
  surface-bright: '#f9faf6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f0'
  surface-container: '#edeeea'
  surface-container-high: '#e7e9e5'
  surface-container-highest: '#e2e3df'
  on-surface: '#1a1c1a'
  on-surface-variant: '#42493e'
  inverse-surface: '#2e312f'
  inverse-on-surface: '#f0f1ed'
  outline: '#72796e'
  outline-variant: '#c2c9bb'
  surface-tint: '#3b6934'
  primary: '#154212'
  on-primary: '#ffffff'
  primary-container: '#2d5a27'
  on-primary-container: '#9dd090'
  inverse-primary: '#a1d494'
  secondary: '#4b6542'
  on-secondary: '#ffffff'
  secondary-container: '#cae9bc'
  on-secondary-container: '#4f6a46'
  tertiary: '#52320b'
  on-tertiary: '#ffffff'
  tertiary-container: '#6d4820'
  on-tertiary-container: '#ecb987'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#bcf0ae'
  primary-fixed-dim: '#a1d494'
  on-primary-fixed: '#002201'
  on-primary-fixed-variant: '#23501e'
  secondary-fixed: '#cdebbe'
  secondary-fixed-dim: '#b1cfa4'
  on-secondary-fixed: '#092005'
  on-secondary-fixed-variant: '#344d2c'
  tertiary-fixed: '#ffdcbd'
  tertiary-fixed-dim: '#f0bd8b'
  on-tertiary-fixed: '#2c1600'
  on-tertiary-fixed-variant: '#623f18'
  background: '#f9faf6'
  on-background: '#1a1c1a'
  surface-variant: '#e2e3df'
typography:
  headline-xl:
    fontFamily: Newsreader
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Newsreader
    fontSize: 32px
    fontWeight: '500'
    lineHeight: '1.3'
  headline-md:
    fontFamily: Newsreader
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 48px
  xl: 80px
  gutter: 24px
  margin: 32px
---

## Brand & Style

The brand personality of this design system is nurturing, expert, and serene. It aims to bridge the gap between scientific accuracy and the hobbyist's passion for nature. The UI should evoke the feeling of a quiet morning in a conservatory—bright, organized, and life-affirming.

The chosen style is **Minimalism with Organic Softness**. By utilizing expansive white space and high-quality botanical imagery, the design system removes digital noise, allowing the user to focus on the plants themselves. The aesthetic avoids harsh geometric rigidity in favor of fluid transitions and soft edges that mimic the natural world.

## Colors

The color palette is rooted in a "Forest to Floor" philosophy. 

- **Primary Green (#2D5A27):** A deep, healthy chlorophyll green used for primary actions and brand emphasis.
- **Secondary Moss (#8DAA81):** A muted, sage-like tone used for secondary UI elements, success states, and subtle backgrounds.
- **Tertiary Clay (#D4A373):** An earthy, warm tone inspired by terracotta pots, used sparingly for accents, notifications, or call-to-action highlights.
- **Neutral Background (#F8F9F5):** A clean, off-white "bone" color that prevents the screen from feeling clinical, providing a softer canvas than pure white.
- **Text (#1A1C19):** A high-contrast dark charcoal with a slight green tint to maintain harmony with the palette.

## Typography

This design system employs a sophisticated pairing of a serif and a sans-serif to achieve a "modern botanical" feel.

- **Headlines (Newsreader):** This serif font provides a literary, authoritative feel reminiscent of classic botany textbooks. Use it for page titles, section headers, and featured quotes to add warmth and character.
- **UI & Body (Plus Jakarta Sans):** A friendly, modern sans-serif that ensures high legibility for plant data, Latin names, and navigation elements. Its slightly rounded terminals complement the organic shape language.
- **Hierarchy:** Maintain large scale differences between headlines and body text to emphasize the airy, editorial layout.

## Layout & Spacing

The layout philosophy follows a **Fixed Grid** system with generous internal padding. A 12-column grid is used for desktop views, but the content width is capped to ensure readability and maintain the "airy" feel.

- **Rhythm:** An 8px base unit drives all spacing decisions. 
- **Margins:** Use wide 32px or 48px margins on the container level to frame the content like a specimen on a page.
- **Whitespace:** Elements are given significant breathing room (using `lg` and `xl` tokens) to prevent the interface from feeling cluttered, even when displaying dense plant data.

## Elevation & Depth

To maintain the fresh, airy feel, this design system avoids heavy shadows. Instead, it utilizes **Ambient Shadows** and **Tonal Layers**.

- **Shadows:** Use extremely soft, diffused shadows with a slight green tint (`rgba(45, 90, 39, 0.05)`) to lift cards off the neutral background. The blur radius should be high (20px+) with low offset.
- **Tonal Layers:** Depth is primarily created by placing `white` cards or containers on the `neutral-color` background. 
- **Interactive Depth:** On hover, elements should slightly increase their shadow spread or shift upwards by 2-4px, simulating a physical lift.

## Shapes

The shape language is defined by **Soft Corners**. There are no sharp 90-degree angles in the primary UI.

- **Components:** Standard buttons and input fields use a 0.5rem (8px) radius.
- **Large Containers:** High-level cards and image containers use `rounded-xl` (1.5rem / 24px) to mimic the soft curves of leaves and petals.
- **Selection States:** Active states or tags should use pill-shaped (fully rounded) geometry to differentiate them from structural containers.

## Components

- **Buttons:** Primary buttons use the Forest Green background with white text. They should have a subtle 1px inner stroke of a lighter green to add "organic" texture. Secondary buttons use a transparent background with a Forest Green border.
- **Cards:** White backgrounds with `rounded-xl` corners. Use subtle ambient shadows. Content inside cards should have at least 24px of padding.
- **Input Fields:** Use a very light grey-green background instead of a harsh border. On focus, the background turns white with a 2px primary green border.
- **Chips / Tags:** Pill-shaped. Used for plant categories (e.g., "Succulent", "Low Light"). Use the Secondary Moss color at 10% opacity with Moss colored text.
- **Plant Identifiers:** Specialized components that highlight leaf patterns or flower colors should use circular image masks to maintain the organic theme.
- **Progress Bars:** For "Growth Tracking," use a thick, rounded track in light moss with the active bar in the primary forest green.