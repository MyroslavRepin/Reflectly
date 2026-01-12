# CSS Architecture Documentation

This project uses a modular CSS architecture that separates styles into logical, maintainable files. All CSS custom properties (variables) are centralized for easy theming and consistency.

## File Structure

```
frontend/static/css/
├── variables.css     # CSS custom properties (colors, spacing, fonts, etc.)
├── base.css          # CSS resets and base element styles
├── layout.css        # Structural layouts (grids, flexbox, containers)
├── components.css    # Component-specific styles (buttons, cards, forms)
├── utilities.css     # Utility classes (margins, padding, text alignment)
└── responsive.css    # Media queries and responsive styles
```

## File Order (CRITICAL)

Always link CSS files in this exact order to maintain proper cascading:

```html
<link rel="stylesheet" href="/static/css/variables.css">
<link rel="stylesheet" href="/static/css/base.css">
<link rel="stylesheet" href="/static/css/layout.css">
<link rel="stylesheet" href="/static/css/components.css">
<link rel="stylesheet" href="/static/css/utilities.css">
<link rel="stylesheet" href="/static/css/responsive.css">
```

**Why this order?**
1. **Variables** must load first - all other files reference these CSS custom properties
2. **Base** sets foundational element styles
3. **Layout** defines structural patterns
4. **Components** builds on layout with specific component styles
5. **Utilities** provides override classes (higher specificity)
6. **Responsive** applies media query overrides last

## File Breakdown

### 1. variables.css
**Purpose:** Centralized design tokens

Contains:
- Color palette (primary, secondary, text, backgrounds)
- Spacing scale (xs to 6xl)
- Typography (font families, sizes, weights, letter-spacing)
- Border radius values
- Shadows
- Transitions
- Z-index layers
- Component sizes (avatars, icons, buttons)

**Usage Example:**
```css
.my-button {
    background: var(--color-primary);
    padding: var(--spacing-md) var(--spacing-lg);
    border-radius: var(--radius-sm);
    transition: all var(--transition-base);
}
```

### 2. base.css
**Purpose:** Reset browser defaults and establish base element styles

Contains:
- Universal box-sizing reset
- HTML/body defaults
- Typography resets (h1-h6, p)
- Link resets
- List resets
- Button/input resets
- Image/SVG display properties

**Key Features:**
- Removes default margins/padding
- Sets consistent box-sizing
- Applies smooth font rendering
- Resets form elements

### 3. layout.css
**Purpose:** Structural layout patterns

Contains:
- Container widths
- Dashboard layout (sidebar + main content)
- Grid systems (projects-grid, clients-grid, features-grid)
- Flexbox layouts (headers, navigation, user profiles)
- Spacing between sections
- Position utilities for structural elements

**Common Patterns:**
- `.dashboard` - Main dashboard flex container
- `.sidebar` - Fixed sidebar navigation
- `.main-content` - Main content area
- `.projects-grid` - Responsive project card grid
- `.hero-content` - Hero section layout

### 4. components.css
**Purpose:** Specific component styles

Contains:
- Navigation (nav-item, nav-icon, nav-links)
- Buttons (btn, btn-start, btn-stop, btn-pause)
- Cards (project-card, hero-card, feature-card, client-card)
- Forms (form-group, form-label, form-input)
- Typography components (titles, subtitles, labels)
- Modals (settings-modal)
- Decorative elements (decorative-plus, status-dot, stars)
- User interface elements (avatar, logo)

**Component Categories:**
- **Buttons:** `.btn`, `.btn-start`, `.btn-stop`, `.btn-pause`, `.btn-save`
- **Cards:** `.hero-card`, `.project-card`, `.feature-card`, `.tracking-card`
- **Forms:** `.form-group`, `.form-label`, `.form-input`, `.checkbox-group`
- **Navigation:** `.nav-item`, `.nav-icon`, `.hamburger`
- **Modals:** `.settings-modal`, `.settings-content`

### 5. utilities.css
**Purpose:** Single-purpose helper classes

Contains:
- Text alignment (text-left, text-center, text-right)
- Display utilities (d-none, d-flex, d-grid)
- Flexbox utilities (justify-center, align-center, gap-md)
- Spacing utilities (mt-xl, mb-lg, p-md)
- Width/height utilities (w-full, h-full)
- Border radius (rounded-sm, rounded-lg, rounded-full)
- Colors (text-primary, bg-white)
- Shadows (shadow-sm, shadow-md, shadow-lg)
- Responsive show/hide classes

**Usage Example:**
```html
<div class="d-flex justify-between align-center gap-lg">
    <h2 class="text-primary font-bold">Title</h2>
    <button class="bg-primary text-white rounded-md">Click</button>
</div>
```

### 6. responsive.css
**Purpose:** Media query breakpoints and responsive overrides

Contains:
- Mobile breakpoints (480px, 768px, 1024px)
- Responsive typography scaling
- Layout adjustments for smaller screens
- Show/hide elements based on screen size
- Print styles
- Accessibility preferences (reduced motion, high contrast)

**Breakpoints:**
- **1024px and below:** Tablet/small desktop adjustments
- **768px and below:** Tablet portrait adjustments
- **480px and below:** Mobile phone adjustments

## CSS Variable Categories

### Colors
```css
--color-primary: #0a0a0a        /* Main black */
--color-secondary: #1a1a1a      /* Secondary black */
--color-white: #ffffff          /* Pure white */
--color-off-white: #e8e8e8      /* Background gray */
--color-text-primary: #000000   /* Primary text */
--color-text-secondary: #666666 /* Secondary text */
--color-error: #dc2626          /* Error red */
--color-success: #22c55e        /* Success green */
```

### Spacing Scale
```css
--spacing-xs: 4px
--spacing-sm: 8px
--spacing-md: 12px
--spacing-lg: 16px
--spacing-xl: 20px
--spacing-2xl: 24px
--spacing-3xl: 30px
--spacing-4xl: 40px
--spacing-5xl: 60px
--spacing-6xl: 80px
```

### Typography
```css
--font-size-xs: 11px
--font-size-sm: 12px
--font-size-base: 13px
--font-size-md: 14px
--font-size-lg: 15px
...up to...
--font-size-10xl: 96px
```

## Best Practices

### 1. Use CSS Variables
✅ **Do:**
```css
.button {
    background: var(--color-primary);
    padding: var(--spacing-md);
}
```

❌ **Don't:**
```css
.button {
    background: #0a0a0a;
    padding: 12px;
}
```

### 2. Use Utility Classes for Simple Styles
✅ **Do:**
```html
<div class="d-flex gap-md mb-xl">
```

❌ **Don't:**
```html
<div style="display: flex; gap: 12px; margin-bottom: 20px;">
```

### 3. Keep Page-Specific Styles Minimal
Only add page-specific styles in `<style>` tags when absolutely necessary. Most styles should use the shared CSS files.

✅ **Do:**
```html
<style>
    /* Only truly unique, non-reusable styles */
    .special-landing-animation {
        /* unique animation */
    }
</style>
```

❌ **Don't:**
```html
<style>
    /* 500 lines of generic styles that should be in components.css */
</style>
```

### 4. Component Naming Convention
Use BEM-inspired naming for related elements:

```css
.card { }
.card-header { }
.card-title { }
.card-body { }
.card-footer { }
```

## Adding New Styles

### When to add to each file:

**variables.css:**
- New color themes
- New spacing values
- New typography scales
- Any reusable design token

**base.css:**
- New element resets
- Global font changes
- Universal box model adjustments

**layout.css:**
- New grid systems
- Container patterns
- Section layouts
- Structural flexbox patterns

**components.css:**
- New UI components
- Component variants
- Complex styled elements

**utilities.css:**
- New helper classes
- Single-purpose styles
- Override utilities

**responsive.css:**
- New breakpoint adjustments
- Mobile-specific overrides
- Print/accessibility styles

## Migration Notes

All three HTML files (`landing.html`, `login-v2.html`, `dashboard-v2.html`) have been migrated to use this CSS structure. The embedded `<style>` tags now only contain page-specific styles (if any).

## Browser Support

This CSS architecture uses modern CSS features:
- CSS Custom Properties (variables)
- CSS Grid
- Flexbox
- CSS `clamp()` for responsive typography

**Minimum browser versions:**
- Chrome 88+
- Firefox 85+
- Safari 14+
- Edge 88+

## Performance

The modular approach provides:
- **Better caching:** Shared CSS files cache across pages
- **Smaller HTML files:** No embedded styles
- **Easier maintenance:** Change once, apply everywhere
- **Better compression:** CSS files compress better than inline styles

## Development Tips

1. **Use browser DevTools** to inspect which CSS file a style comes from
2. **Search across CSS files** to find where a class is defined
3. **Use CSS variable inspector** in DevTools to see all available variables
4. **Test responsive breakpoints** using browser responsive design mode
5. **Validate CSS** periodically to catch errors

## Future Enhancements

Consider adding:
- **animations.css** - Complex animations and keyframes
- **themes.css** - Dark mode and alternative color schemes
- **print.css** - Dedicated print styles
- **vendors.css** - Third-party library overrides

## Questions?

For questions or suggestions about the CSS architecture, please refer to the project's code standards and best practices documentation.

