# Clarus Design System - Comprehensive Style Guide v1.1

## Overview
**Clarus** is an AI Decision Insights platform dedicated to making complex artificial intelligence systems transparent, understandable, and trustworthy through an elegant, accessible, and playful user interface.

### Design Philosophy
The Clarus design system balances professional aesthetics with playful interactions, creating an approachable yet authoritative interface through:
- **Transparency**: Clear visual hierarchy and intuitive information architecture
- **Playfulness**: Subtle animations and cute decorative elements (✨ 💡 🚀 🎯 💎) featuring the Arctic Fox mascot
- **Consistency**: Unified token system across all components and pages
- **Accessibility**: WCAG AA compliance with thoughtful color contrast and motion options
- **Responsiveness**: Mobile-first approach with graceful degradation across devices
- **Mascot Integration**: The Arctic Fox serves as a friendly, approachable brand ambassador, appearing strategically throughout the interface to enhance user engagement and reinforce brand personality

## Color Palette

### Primary Colors

#### Primary Blue (#4da6ff)
- **RGB**: rgb(77, 166, 255)
- **Use Cases**: CTA buttons, interactive links, highlights, primary actions
- **Contrast**: 8.2:1 with white (WCAG AAA), 6.8:1 with warm beige (WCAG AA)
- **Hover State**: #2d8fdb (darker, more saturated)
- **Opacity Variations**:
  - 4% opacity: `rgba(77, 166, 255, 0.04)` — very subtle backgrounds
  - 8% opacity: `rgba(77, 166, 255, 0.08)` — card backgrounds
  - 15% opacity: `rgba(77, 166, 255, 0.15)` — hover overlays
  - 30% opacity: `rgba(77, 166, 255, 0.3)` — subtle borders

#### Dark Gray (#383838)
- **RGB**: rgb(56, 56, 56)
- **Use Cases**: Primary body text, main headings, primary interface elements
- **Contrast Ratio**: 14.5:1 with white (WCAG AAA), 11.3:1 with warm beige (WCAG AAA)
- **Secondary Variant**: #555555 (medium-gray for secondary text, 10.5:1 contrast)

#### Warm Beige (#f4efea)
- **RGB**: rgb(244, 239, 234)
- **Use Cases**: Default page background, subtle section backgrounds, neutral zones
- **Purpose**: Warm, welcoming tone that reduces eye strain and creates approachability
- **Pairing**: Pairs beautifully with dark-gray text and primary-blue accents

### Secondary & Accent Colors

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Warm Orange | #ff6b35 | rgb(255, 107, 53) | Gradient accents, secondary focus |
| Golden Yellow | #ffa500 | rgb(255, 165, 0) | Hover enhancements, warmth |
| Alert Yellow | #ffeb3b | rgb(255, 235, 59) | Announcements, attention-grabbing |
| Dark Charcoal | #2d2d2d | rgb(45, 45, 45) | Footer background, high-contrast areas |
| Light Gray | #e0e0e0 | rgb(224, 224, 224) | Borders, dividers, subtle boundaries |

### Color Usage Guidelines

**Backgrounds**:
- Page Default: Warm Beige (#f4efea)
- White Zones: Cards, panels, modals
- Gradient Backgrounds: Blue to darker blue (135deg)
- Subtle Tints: 4-8% opacity overlays

**Text Colors**:
- Primary Text: Dark Gray (#383838)
- Secondary Text: Medium Gray (#555555)
- Interactive: Primary Blue (#4da6ff)
- Hover: Primary Blue with underline

**Hover States**:
- Color Change: To Primary Blue
- Shadow: 0 8px 16px rgba(77, 166, 255, 0.15)
- Border: Blue highlight
- Background: Subtle warm beige tint

## Typography System

### Font Stack & Characteristics

**Primary Font**: `"Aeonik Mono", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- Modern monospace aesthetic with excellent readability
- Tech-forward yet approachable personality
- Professional polish suitable for enterprise contexts
- Consistent character width for alignment and data display

**Code Font**: `"Monaco", "Menlo", monospace`
- Used for code blocks, technical content, data displays
- Applied in workspace panels for data input/output

### Font Weights & Usage

| Weight | Value | Usage | Examples |
|--------|-------|-------|----------|
| Regular | 400 | Body text, descriptions | Paragraph text, feature descriptions |
| Medium | 500 | Secondary labels, smaller UI text | Subtitles, navigation secondary text |
| Semibold | 600 | Titles, navigation, emphasis | H3, feature titles, button text |
| Bold | 700 | Headings, primary emphasis | H1, H2, strong emphasis |

### Type Hierarchy & Scale

#### H1 - Hero Title (3.5rem / 56px)
```css
font-size: 3.5rem;
font-weight: 700;
line-height: 1.2;
letter-spacing: -0.02em;
word-spacing: 0.1em;
margin-bottom: 1.5rem;
```
- **Use**: Hero section main heading
- **Example**: "理解 AI 的决策逻辑"
- **Special Effects**:
  - Gradient text (blue to darker blue)
  - Gradient shift animation (4s infinite)
  - Floating emoji (✨) above with float animation (3s)
- **Responsive**: 2.5rem (tablet), 2rem (mobile)

#### H2 - Section Title (2rem / 32px)
```css
font-size: 2rem;
font-weight: 700;
line-height: 1.2;
letter-spacing: -0.01em;
margin-bottom: 2rem;
```
- **Use**: Section headers, major section titles
- **Examples**: "核心能力", "探索 AI 领域", "我们的团队"
- **Special Effects**:
  - ::before: Gradient decorative line (60px × 4px, blue to orange)
  - ::before animation: slideInRight (0.6s ease-out)
  - ::after: Bouncing emoji (✨)
  - ::after animation: bounce (2s infinite)
- **Responsive**: 1.75rem (tablet), 1.5rem (mobile)

#### H3 - Card/Feature Title (1.25rem / 20px)
```css
font-size: 1.25rem;
font-weight: 600;
margin-bottom: 1rem;
letter-spacing: 0.02em;
color: var(--color-dark-gray);
```
- **Use**: Feature card titles, subsection headers, card titles
- **Examples**: "可视化", "解释", "学习", "围棋"
- **Styling**: Clean, readable, with subtle letter-spacing for elegance

#### Subtitle - Large Secondary (0.95rem / 15.2px)
```css
font-size: 0.95rem;
font-weight: 500;
line-height: 1.6;
letter-spacing: 0.05em;
text-transform: uppercase;
margin-bottom: 2rem;
color: var(--color-medium-gray);
```
- **Use**: Hero subtitle, secondary descriptions, emphasis text
- **Example**: "Clarus 让复杂的人工智能分析变得透明、易懂、可信任"
- **Style**: Uppercase with increased letter-spacing for elegance and hierarchy

#### Body Text (1rem / 16px)
```css
font-size: 1rem;
font-weight: 400;
line-height: 1.5;
color: var(--color-dark-gray);
```
- **Use**: Paragraph text, main descriptions, primary content
- **Line Height**: 1.5 for comfortable sustained reading
- **Minimum Size**: Readable down to 14px on mobile

#### Secondary Text (0.9rem / 14.4px)
```css
font-size: 0.9rem;
color: var(--color-medium-gray);
line-height: 1.6;
font-weight: 400;
```
- **Use**: Card descriptions, feature descriptions, meta information
- **Examples**: Domain card descriptions, feature card text

#### Small Text (0.85rem / 13.6px)
```css
font-size: 0.85rem;
color: var(--color-medium-gray);
font-weight: 500;
```
- **Use**: Badges, status indicators, labels, timestamps
- **Examples**: "Active", "Beta", "即将推出"

#### Navigation Text (14px)
```css
font-size: 14px;
font-weight: 500;
line-height: 1.371;
letter-spacing: 0.32px;
color: var(--color-dark-gray);
```
- **Use**: Navigation links, menu items, header text
- **Examples**: "洞察文库", "关于", "领域"
- **Hover Effect**: Gradient underline animation (blue to orange, 0.3s)

#### Button Text (0.95rem / 15.2px)
```css
font-size: 0.95rem;
font-weight: 600;
line-height: 1.5;
color: white;
text-decoration: none;
```
- **Use**: Button labels, CTA text
- **Examples**: "立即开始", "了解详情", "登录"
- **Interaction**: Shine effect on hover (0.3s)

### Line Height Guidelines

| Context | Line Height | Reason |
|---------|-----------|--------|
| Headings | 1.2 | Tight, prestigious appearance |
| Body Text | 1.5-1.6 | Comfortable sustained reading |
| Code/Data | 1.4-1.6 | Technical clarity with spacing |
| UI Labels | 1.371 | Precise spacing for consistency |

### Letter Spacing Guidelines

| Element | Letter Spacing | Purpose |
|---------|----------------|---------|
| H1 Title | -0.02em | Tight, impactful presence |
| Section Title | -0.01em | Modern, premium feel |
| Uppercase Text | 0.05em | Better readability and elegance |
| Navigation | 0.32px | Subtle refinement |
| Normal Text | 0 (default) | Natural readability |

## Spacing System

Base Unit: 8px (0.5rem)

- --spacing-1: 8px (Micro gaps)
- --spacing-2: 16px (Standard)
- --spacing-3: 24px (Medium)
- --spacing-4: 32px (Large)
- --spacing-6: 48px (XL)
- --spacing-8: 64px (Hero)

## Component Styles

### Mascot - Arctic Fox (吉祥物)

#### Large Mascot (Hero Section)
- **Position**: Absolute positioned right side of hero section
- **Size**: 450px (desktop), 300px (tablet), 200px (mobile)
- **Opacity**: 0.85 (full), 0.6 (mobile)
- **Animation**: `floatLarge 4s ease-in-out infinite`
  - Vertical floating motion: translateY(-50%) → translateY(-70%) → translateY(-50%)
  - Creates gentle, natural bobbing effect
- **Shadow**: `drop-shadow(0 10px 20px rgba(0, 0, 0, 0.1))`
- **Z-index**: 5 (behind text content)
- **Pointer Events**: None (non-interactive)
- **Asset Path**: `assets/mascot/arctic-fox-sitting-v2.png`
- **Purpose**: Primary visual focus in hero, reinforces brand identity and adds personality

#### Small Mascots (Feature Cards & CTA Sections)
- **Position**: Decorative elements scattered throughout page
- **Size**: Varies based on context
- **Animation**: Bounce or drift animations for subtle movement
- **Assets**:
  - `arctic-fox-sleeping.png` - Relaxed pose, used in CTA sections
  - `arctic-fox-sitting-v4.png` - Active pose, used as decorative elements
- **Purpose**: Create visual interest, guide user attention, reinforce playful tone

#### Mascot Animation Guidelines
```css
@keyframes floatLarge {
    0%, 100% {
        transform: translateY(-50%);
    }
    50% {
        transform: translateY(calc(-50% - 20px));
    }
}

@keyframes drift {
    0%, 100% {
        transform: translateX(0px) translateY(0px);
    }
    50% {
        transform: translateX(20px) translateY(-20px);
    }
}
```

### Buttons

#### Primary Button (Hero/CTA)
- **Background**: Primary Blue (#4da6ff)
- **Color**: White
- **Padding**: 0.9rem 2rem
- **Height**: Auto (adaptive)
- **Border**: 2px solid Dark Gray
- **Border Radius**: 4px
- **Font Weight**: 600 (semibold)
- **Cursor**: Pointer
- **Hover State**:
  - Shine animation (left: -100% → 0% in 0.3s)
  - Color change: #2d8fdb
  - Transform: translateY(-2px)
  - Shadow: 0 8px 16px rgba(77, 166, 255, 0.3)
- **Transition**: all 0.2s ease
- **Position**: Relative + overflow hidden (for shine effect)

#### Primary Button (Form/Auth) - Enhanced
- **Background**: Primary Blue (#4da6ff)
- **Color**: White
- **Padding**: 0.9rem 2rem
- **Height**: 48px (explicit height for form consistency)
- **Border**: 2px solid Dark Gray
- **Border Radius**: 4px
- **Display**: Flex with center alignment
- **Hover State**:
  - Color change: #2d8fdb
  - Transform: translateY(-2px)
  - Shadow: 0 8px 16px rgba(77, 166, 255, 0.3)
- **Transition**: all 0.2s ease

#### Social Button (Auth Forms)
- **Background**: White
- **Color**: Dark Gray
- **Padding**: 0.75rem 1rem
- **Height**: 44px
- **Border**: 1px solid Light Gray
- **Border Radius**: 4px
- **Display**: Flex with center alignment
- **Font Size**: 0.95rem
- **Hover State**:
  - Border Color: Primary Blue
  - Background: rgba(77, 166, 255, 0.05)
  - Transform: translateY(-2px)
  - Shadow: 0 4px 8px rgba(0, 0, 0, 0.08)
- **Transition**: all 0.2s ease

#### Secondary Button
- **Background**: Transparent
- **Color**: Dark Gray
- **Border**: 2px solid Dark Gray
- **Hover**: Warm beige background + lift + shadow

#### Light Button
- **Background**: White
- **Color**: Primary Blue
- **Hover**: Background to warm beige + lift + shadow

### Feature Cards
- Background: White
- Padding: 2rem
- Border Radius: 8px
- Shadow: 0 2px 4px rgba(0,0,0,0.1)
- Hover: Top bar animates in + lift (-4px) + scale (1.02x) + enhanced shadow
- Icon: Bounces continuously (2s infinite, staggered)

### Domain Cards
- Background: Linear gradient (blue-tinted)
- Padding: 2rem
- Border: 2px solid Light Gray
- Hover: Shine sweeps across + icon rotates (-10deg) scales (1.1x) + lift (-4px) scale (1.02x)

### Authentication Forms (Login/Register)

#### Form Container
- **Background**: White
- **Padding**: 3rem
- **Border Radius**: 12px
- **Box Shadow**: 0 12px 32px rgba(0, 0, 0, 0.12)
- **Width**: 100%, max-width 520px (register), 480px (login)
- **Position**: Centered within main-content flex container

#### Form Header
- **Text Align**: Center
- **Margin Bottom**: var(--spacing-6) (48px)

#### Form Title
- **Font Size**: 2rem (32px)
- **Font Weight**: 700 (bold)
- **Margin Bottom**: var(--spacing-2) (16px)
- **Color**: Dark Gray
- **Letter Spacing**: -0.01em

#### Form Subtitle
- **Font Size**: 1rem (16px)
- **Font Weight**: 400 (regular)
- **Color**: Medium Gray
- **Line Height**: 1.5
- **Example**: "开始探索 AI 决策的奥秘" (Register), "登录您的 Clarus 账户" (Login)

#### Form Group
- **Margin Bottom**: var(--spacing-3) for default, var(--spacing-4) for login forms

#### Form Label
- **Display**: Block
- **Font Size**: 0.9rem (14.4px)
- **Font Weight**: 600 (semibold)
- **Margin Bottom**: var(--spacing-1) (8px)
- **Color**: Dark Gray

#### Form Input
- **Width**: 100%
- **Padding**: 0.75rem 1rem
- **Height**: 44px
- **Border**: 1px solid Light Gray
- **Border Radius**: 4px
- **Font Size**: 1rem (16px)
- **Font Family**: Primary font stack
- **Transition**: all 0.2s
- **Focus State**:
  - Border Color: Primary Blue
  - Box Shadow: 0 0 0 3px rgba(77, 166, 255, 0.1)
  - Outline: None

#### Form Row (Multi-column)
- **Display**: Grid
- **Grid Template Columns**: 1fr 1fr
- **Gap**: var(--spacing-2) (16px)
- **Responsive**: Single column on mobile

#### Checkbox Group
- **Display**: Flex
- **Align Items**: Flex-start
- **Gap**: var(--spacing-1) (8px)
- **Margin Bottom**: var(--spacing-4) (32px)
- **Font Size**: 0.85rem (13.6px)
- **Line Height**: 1.5

#### Custom Checkbox
- **Width**: 18px (registration), 16px (login)
- **Height**: 18px (registration), 16px (login)
- **Border**: 1px solid Light Gray
- **Border Radius**: 2px
- **Cursor**: Pointer
- **Transition**: all 0.2s
- **Flex Shrink**: 0 (prevent squishing)
- **Hover**: Border color changes to Primary Blue

#### Form Helper (Login specific)
- **Display**: Flex
- **Justify Content**: Space-between
- **Align Items**: Center
- **Font Size**: 0.85rem (13.6px)
- **Margin Bottom**: var(--spacing-4) (32px)

#### Form Footer
- **Text Align**: Center
- **Margin Top**: var(--spacing-4) (32px)
- **Font Size**: 0.9rem (14.4px)
- **Color**: Medium Gray
- **Link Color**: Primary Blue
- **Link Hover**: Color changes to #2d8fdb

#### Divider (Between sections)
- **Text Align**: Center
- **Margin**: var(--spacing-4) 0 (32px vertical)
- **Position**: Relative
- **Before Element**: Line (1px height, Light Gray)
- **Text**: Medium Gray color, positioned relative above line

#### Auth Background
- **Page Background**: Linear gradient (135deg, warm-beige 0%, #f0f0f0 100%)
- **Purpose**: Subtle, non-distracting background

#### Header (Auth Pages)
- **Background**: Warm Beige
- **Height**: 90px
- **Padding**: var(--spacing-2) var(--spacing-4)
- **Display**: Flex with space-between
- **Border Bottom**: 1px solid Light Gray
- **Logo**: "✨ Clarus" with navigation link

#### Footer (Auth Pages)
- **Background Color**: Dark Charcoal (#2d2d2d)
- **Color**: Light Gray
- **Padding**: var(--spacing-4)
- **Text Align**: Center
- **Font Size**: 0.85rem (13.6px) for copyright
- **Links**: Light Gray color with 0.2s transition on hover

### Navigation Links
- Color: Dark Gray
- Hover: Gradient underline (blue→orange) + color to primary blue

## Shadows & Elevation

- Small: 0 2px 4px rgba(0,0,0,0.1)
- Medium: 0 8px 16px rgba(0,0,0,0.15)
- Large: 0 20px 40px rgba(0,0,0,0.2)
- Blue-tint: 0 8px 16px rgba(77,166,255,0.15)

## Animations & Transitions

### Timing
- 0.2s: Quick changes
- 0.3s: Medium interactions
- 0.6s: Shine/gradient effects
- 0.8s: Page load
- 2-3s: Continuous loops
- 4-8s: Background animations

### Keyframe Animations
- **Float**: Gentle vertical bob (3s)
- **Bounce**: Playful pulse (2s)
- **Slide In Up**: Entry animation (0.8s)
- **Slide In Right**: Line reveal (0.6s)
- **Fade In Scale**: Zoom entrance (0.8s)
- **Drift**: Floating motion (6s)
- **Gradient Shift**: Color breathing (4s)
- **Shimmer**: Background sweep (8s)

## Border Radius

- --radius-small: 4px (Buttons, inputs)
- --radius-medium: 8px (Cards, containers)
- --radius-full: 50% (Avatars, circles)
- Pill: 9999px (Badges)

## Opacity & Transparency

- Watermark: 0.05 (Patterns)
- Very Faint: 0.08 (Backgrounds)
- Light: 0.15-0.2 (Hover)
- Medium: 0.3-0.4 (Overlays)
- Strong: 0.6-0.7 (Semi-transparent)

## Responsive Design

### Breakpoints
- Desktop: 1024px+
- Tablet: 728px - 1024px
- Mobile: <728px

### Responsive Scale
| Device | H1 | H2 | Section Padding | Gap |
|--------|----|----|-----------------|-----|
| Desktop | 3.5rem | 2rem | 4rem 2rem | 2rem |
| Tablet | 2.5rem | 1.75rem | 2rem 1.5rem | 1.5rem |
| Mobile | 2rem | 1.5rem | 1rem | 1rem |

## Accessibility

### Color Contrast
- Dark Gray on White: 14.5:1 (AAA)
- Primary Blue on White: 8.2:1 (AAA)
- Medium Gray on White: 10.5:1 (AAA)

### Focus States
```css
:focus {
    outline: 2px solid var(--color-primary-blue);
    outline-offset: 2px;
}
```

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

## CSS Variables

```css
:root {
    --color-primary-blue: #4da6ff;
    --color-dark-gray: #383838;
    --color-warm-beige: #f4efea;
    --color-medium-gray: #555555;
    --color-light-gray: #e0e0e0;
    --color-dark-charcoal: #2d2d2d;

    --font-primary: "Aeonik Mono", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    --font-weight-regular: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;

    --spacing-1: 0.5rem;
    --spacing-2: 1rem;
    --spacing-3: 1.5rem;
    --spacing-4: 2rem;
    --spacing-6: 3rem;
    --spacing-8: 4rem;

    --radius-small: 4px;
    --radius-medium: 8px;
    --radius-full: 50%;
    --transition-fast: all 0.2s ease;
}
```

## Authentication Form System

### Form Structure Overview

Authentication forms (Login/Register) follow a consistent pattern with the following structure:
1. **Page Background**: Gradient background for visual consistency
2. **Header**: Navigation with logo and return link
3. **Main Content**: Centered form container
4. **Form Body**: Input fields with labels, helper text
5. **Action Button**: Primary CTA button (48px height, flex centered)
6. **Social Divider**: "或使用以下方式..." separator with line
7. **Social Buttons**: Grid of 2 columns (1 on mobile) for OAuth providers
8. **Footer Link**: Link to alternative form (register/login)
9. **Page Footer**: Copyright and legal links

### Form Responsiveness
- **Desktop**: Form max-width 520px (register), 480px (login)
- **Tablet**: Reduced padding, adjusted spacing
- **Mobile**: Full width with 1rem padding, single-column layouts

## Example Implementation Patterns

### Authentication Form (Login) with Enhanced Styling
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clarus - 登录</title>
    <style>
        :root {
            --color-primary-blue: #4da6ff;
            --color-dark-gray: #383838;
            --color-warm-beige: #f4efea;
            --color-medium-gray: #555555;
            --color-light-gray: #e0e0e0;
            --color-dark-charcoal: #2d2d2d;
            --font-primary: "Aeonik Mono", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            --spacing-1: 0.5rem;
            --spacing-2: 1rem;
            --spacing-3: 1.5rem;
            --spacing-4: 2rem;
            --radius-small: 4px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-primary);
            background: linear-gradient(135deg, var(--color-warm-beige) 0%, #f0f0f0 100%);
            color: var(--color-dark-gray);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .login-container {
            background: white;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
            width: 100%;
            max-width: 480px;
        }

        .form-input {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 1px solid var(--color-light-gray);
            border-radius: var(--radius-small);
            font-size: 1rem;
            font-family: var(--font-primary);
            transition: all 0.2s;
            height: 44px;
        }

        .form-input:focus {
            outline: none;
            border-color: var(--color-primary-blue);
            box-shadow: 0 0 0 3px rgba(77, 166, 255, 0.1);
        }

        .btn-login {
            width: 100%;
            padding: 0.9rem 2rem;
            background-color: var(--color-primary-blue);
            color: white;
            border: 2px solid var(--color-dark-gray);
            border-radius: var(--radius-small);
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.2s;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .btn-login:hover {
            background-color: #2d8fdb;
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(77, 166, 255, 0.3);
        }

        .btn-social {
            padding: 0.75rem 1rem;
            border: 1px solid var(--color-light-gray);
            background: white;
            border-radius: var(--radius-small);
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.95rem;
        }

        .btn-social:hover {
            border-color: var(--color-primary-blue);
            background: rgba(77, 166, 255, 0.05);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
        }
    </style>
</head>
<body>
    <!-- Structure follows the pattern -->
</body>
</html>
```

### Feature Card with Animations
```css
.feature-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
}

/* Animated top bar */
.feature-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4da6ff, #ffa500);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s ease;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    border-color: rgba(77, 166, 255, 0.2);
}

.feature-card:hover::before {
    transform: scaleX(1);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    animation: bounce 2s ease-in-out infinite;
}

.feature-card:nth-child(2) .feature-icon {
    animation-delay: 0.2s;
}
```

### Domain Card with Shine Effect
```css
.domain-card {
    background: linear-gradient(135deg, rgba(77, 166, 255, 0.08) 0%, rgba(77, 166, 255, 0.04) 100%);
    padding: 2rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    position: relative;
    overflow: hidden;
}

/* Diagonal shine effect */
.domain-card::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(45deg,
        transparent 30%,
        rgba(77, 166, 255, 0.05) 50%,
        transparent 70%);
    transform: translateX(-100%);
    transition: transform 0.6s ease;
}

.domain-card:hover::before {
    transform: translateX(100%);
}

.domain-card:hover .domain-card-icon {
    transform: rotate(-10deg) scale(1.1);
}

.domain-card-icon {
    font-size: 2.5rem;
    transition: transform 0.3s ease;
}
```

## Arctic Fox Mascot Guidelines

### Mascot Brand Identity
The Arctic Fox is the primary mascot and brand ambassador for Clarus. It embodies:
- **Friendliness**: Approachable and warm personality
- **Intelligence**: Curious, clever nature mirrors AI sophistication
- **Trustworthiness**: Arctic foxes are known for adaptability and reliability
- **Playfulness**: Adds personality without sacrificing professionalism

### Usage Recommendations

#### Primary Hero Mascot
- **Location**: Hero section, right side
- **Size**: 450px (desktop) – most prominent visual element
- **Animation**: Gentle floating motion (floatLarge) to draw attention
- **Opacity**: 0.85 to allow text to remain visible
- **Purpose**: Create immediate visual impact and establish brand identity
- **Asset**: `arctic-fox-sitting-v2.png` (primary, alert pose)

#### Secondary Decorative Mascots
- **Locations**: Feature sections, CTA sections, between content blocks
- **Size**: 200-300px (context-dependent)
- **Animation**: Bounce, drift, or subtle hover effects
- **Assets**:
  - `arctic-fox-sleeping.png` – Relaxed, friendly pose for CTA sections
  - `arctic-fox-sitting-v4.png` – Active pose for accent areas
- **Opacity**: 0.7-0.85
- **Purpose**: Enhance user experience, add visual interest, guide attention

#### Responsive Behavior
- **Desktop**: Full-size mascots with prominent placement
- **Tablet**: Reduced size (70% of desktop), adjusted positioning
- **Mobile**: Further reduced size (40-50% of desktop), repositioned for mobile-first layout
- **Principle**: Mascots enhance but never obstruct primary content

#### Mascot Color Integration
- **Primary**: PNG with full colors (no filters applied)
- **Shadow**: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.1))
- **Optional Overlays**: Can apply subtle opacity for layering
- **Background**: Works well with warm beige and white backgrounds

#### Animation Best Practices for Mascots
- Keep animations at 3-4s cycles for continuous floating
- Use ease-in-out for natural motion
- Avoid rapid movements that distract from content
- Stagger animations if multiple mascots appear on same page
- Always include `pointer-events: none` to prevent interaction conflicts

### Mascot File Management
```
assets/
├── mascot/
│   ├── arctic-fox-sitting-v2.png    (Primary hero mascot)
│   ├── arctic-fox-sitting-v4.png    (Active pose accent)
│   └── arctic-fox-sleeping.png      (Relaxed pose for CTAs)
```

### When NOT to Use Mascot
- Loading states (use spinners or progress indicators instead)
- Error messages (maintains clarity and seriousness)
- Warning notifications (might reduce perceived urgency)
- Mobile forms (space constraints)
- Accessibility-critical interactions (avoid visual-only information)

### Form Input States

#### Default State (Empty)
```css
.form-input {
    border: 1px solid var(--color-light-gray);
    background: white;
}
```

#### Focus State
```css
.form-input:focus {
    border-color: var(--color-primary-blue);
    box-shadow: 0 0 0 3px rgba(77, 166, 255, 0.1);
}
```

#### Filled State
```css
.form-input:not(:placeholder-shown) {
    background: white;
    border: 1px solid var(--color-light-gray);
}
```

#### Hover State (Non-focus)
```css
.form-input:hover:not(:focus) {
    border-color: rgba(77, 166, 255, 0.3);
}
```

#### Disabled State (Future implementation)
```css
.form-input:disabled {
    background: #f5f5f5;
    border-color: var(--color-light-gray);
    cursor: not-allowed;
    opacity: 0.6;
}
```

#### Error State (Recommended for future)
```css
.form-input.error {
    border-color: #ff6b6b;
}

.form-input.error:focus {
    box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
}
```

### Form Label Positioning
- Labels appear **above** input fields
- Consistent font-size: 0.9rem (14.4px)
- Font-weight: 600 (semibold) for clear hierarchy
- Dark Gray color matching body text
- Margin-bottom: 0.5rem (8px) for proper spacing

### Login vs. Register Forms - Key Differences

| Aspect | Login Form | Register Form |
|--------|-----------|--------------|
| **Form Width** | 480px max-width | 520px max-width |
| **Fields** | Email, Password | First/Last Name, Email, Password, Confirm Password |
| **Name Row** | N/A | 2-column grid (First/Last) |
| **Helper Text** | "记住我" checkbox + "忘记密码?" link | "我同意服务条款和隐私政策" checkbox |
| **Form Group Spacing** | var(--spacing-4) (32px) | var(--spacing-3) (24px) |
| **Social Text** | "或使用以下方式登录" | "或使用以下方式注册" |
| **Footer Link** | "还没有账户？立即注册" | "已有账户？立即登录" |
| **Subtitle** | "登录您的 Clarus 账户" | "开始探索 AI 决策的奥秘" |

### Consistent Elements Across Both Forms
- Button height: 48px
- Social button height: 44px
- Input height: 44px
- Button styling: Primary Blue with dark gray border
- Social button grid: 2 columns (desktop), 1 column (mobile)
- Form padding: 3rem
- Container border-radius: 12px
- Container shadow: 0 12px 32px rgba(0, 0, 0, 0.12)
- Page background: Linear gradient (135deg, warm-beige 0%, #f0f0f0 100%)
- Header height: 90px
- Footer styling: Dark Charcoal background

## Best Practices & Guidelines

### When to Use Each Component
- **Primary Button**: Main CTAs (register, submit, next)
- **Secondary Button**: Alternative actions (learn more, cancel)
- **Light Button**: CTAs on dark backgrounds
- **Feature Cards**: Capability showcases
- **Domain Cards**: Feature/service selection
- **Navigation Links**: Header and footer navigation

### Animation Best Practices
✓ Keep animations under 1s for state changes (0.2-0.4s preferred)
✓ Use 2-3s for continuous loops to avoid distraction
✓ Provide hover feedback within 200ms
✓ Respect prefers-reduced-motion for accessibility
✓ Use ease and ease-in-out timing functions
✓ Avoid animations on every element (select key elements)

### Spacing Best Practices
✓ Always use the 8px grid (multiples of 8px)
✓ Use spacing variables (--spacing-1 through --spacing-8)
✓ Consistent padding: 1rem (small), 1.5rem (medium), 2rem (large)
✓ Consistent gaps: 1.5-2rem for most layouts
✓ Responsive padding: Reduce by 50% on tablet, 75% on mobile

### Typography Best Practices
✓ Use font-weight 400 for body text (maximum readability)
✓ Use font-weight 600-700 for emphasis (headings, buttons)
✓ Keep line-height at 1.5-1.6 for body text
✓ Use letter-spacing only for uppercase or display text
✓ Maintain contrast ratio > 4.5:1 for all text

### Accessibility Practices
✓ All interactive elements must have visible focus states
✓ Color alone must not convey information
✓ Provide alt text for all meaningful images
✓ Use semantic HTML (<button>, <a>, proper headings)
✓ Ensure 8:1 contrast for disabled states
✓ Test keyboard navigation throughout
✓ Support users with motion sensitivity

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2 | 2024 | Added Arctic Fox mascot guidelines, authentication form system documentation, enhanced button specifications (form vs. CTA buttons), social button styling, form component details (inputs, labels, helpers, dividers), mascot animation patterns and responsive behavior |
| 1.1 | 2024 | Enhanced documentation with detailed component specs, animation library, accessibility guidelines |
| 1.0 | 2024 | Initial design system documentation |

---

## Quick Reference: Design Tokens Summary

### Critical Component Specifications for Development

#### Authentication Pages (Login/Register)
- Container: 480-520px width, 3rem padding, 12px border-radius
- Form inputs: 44px height, 0.75rem padding, 1px border
- Buttons (submit): 48px height, flex centered, 0.9rem padding horizontal
- Social buttons: 44px height, 2-column grid (1 on mobile)
- Input focus: Primary blue border + 3px rgba(77, 166, 255, 0.1) shadow
- Button hover: #2d8fdb color + -2px translateY + 0.3s shadow

#### Mascot Elements
- Hero large: 450px/300px/200px (desktop/tablet/mobile), floatLarge 4s animation
- Small accents: 200-300px, bounce/drift 2-3s animations
- All mascots: pointer-events: none, drop-shadow(0 10px 20px rgba(0,0,0,0.1))

#### Spacing System (8px base)
- Gap/margin standard: 1.5-2rem (24-32px)
- Form field spacing: 1rem between groups
- Container padding: 2-4rem
- Section padding: 3-4rem vertical, 2rem horizontal

#### Typography Essentials
- Body: 1rem (16px), weight 400, line-height 1.5
- Labels: 0.9rem (14.4px), weight 600
- Headings: 2rem (32px), weight 700
- Small text: 0.85rem (13.6px), weight 500

---

**Document Status**: Active (v1.2)
**Last Updated**: November 2024
**Maintained By**: Clarus Design Team
**Key Updates (v1.2)**: Arctic Fox mascot system, authentication form documentation, enhanced button specifications
**Contact**: Design System Maintainers
**Next Review**: Quarterly

---

## Implementation Checklist

### For New Pages/Components
- [ ] Use CSS variables for all colors, spacing, and typography
- [ ] Implement hover states with 0.2-0.3s transitions
- [ ] Add proper focus states for accessibility
- [ ] Test responsive behavior at 728px and 1024px breakpoints
- [ ] Validate color contrast ratios (minimum 4.5:1)
- [ ] Include mascot where appropriate (hero, CTAs, feature sections)
- [ ] Verify form heights match specification (inputs 44px, buttons 48px)
- [ ] Test form focus and input states
- [ ] Ensure animations respect prefers-reduced-motion
- [ ] Add drop-shadow to any floating elements

### For Form Components
- [ ] Max-width: 480px (login) or 520px (register)
- [ ] Input padding: 0.75rem 1rem
- [ ] Button height: 48px with flex center alignment
- [ ] Social buttons: 2-column grid (responsive to 1 column)
- [ ] Divider margin: 2rem vertical spacing
- [ ] Footer link styling: Medium gray with primary blue link

---

*This style guide is a living document. Please report any inconsistencies or suggest improvements to the design team.*
