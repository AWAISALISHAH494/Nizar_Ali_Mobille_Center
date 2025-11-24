# Military Date Picker - Complete Guide

## Overview
The Military Date Picker is a custom, beautifully designed date picker component with military-themed styling that provides an exceptional user experience for date selection across your e-commerce website.

## Features

### 🎨 **Visual Design**
- **Military Theme**: Military green gradients (#3d5a40 to #556b2f)
- **Smooth Animations**: Hover effects, transitions, and selection animations
- **Responsive Design**: Works perfectly on all devices
- **Modern UI**: Rounded corners, shadows, and premium styling

### ⚡ **Functionality**
- **Quick Date Selection**: Today, Tomorrow, Next Week, Next Month, Next Year
- **Time Support**: Full date and time selection with 12/24 hour formats
- **Date Validation**: Min/max date restrictions
- **Keyboard Navigation**: Full keyboard support
- **Touch Friendly**: Optimized for mobile devices

### 🔧 **Technical Features**
- **Auto-initialization**: Automatically converts all date inputs
- **Manual Control**: JavaScript API for custom implementations
- **Form Integration**: Works seamlessly with Django forms
- **Accessibility**: ARIA labels and keyboard navigation

## Usage

### Basic HTML
```html
<!-- Basic Date Picker -->
<input type="date" class="form-control datepicker" placeholder="Choose a date">

<!-- DateTime Picker -->
<input type="datetime-local" class="form-control datetime-picker" placeholder="Select date and time">
```

### Django Forms
```python
# In your forms.py
class MyForm(forms.Form):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    event_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control datetime-picker'}))
```

```html
<!-- In your template -->
{% load ui_extras %}
{{ form.birth_date|add_class:"form-control datepicker" }}
{{ form.event_datetime|add_class:"form-control datetime-picker" }}
```

### JavaScript API
```javascript
// Manual initialization
const datePicker = new MilitaryDatePicker(inputElement, {
    format: 'yyyy-mm-dd',
    showTime: true,
    timeFormat: '24',
    quickDates: true,
    minDate: new Date(),
    maxDate: new Date(2025, 11, 31)
});

// Available options
const options = {
    format: 'yyyy-mm-dd',           // Date format
    minDate: null,                  // Minimum selectable date
    maxDate: null,                  // Maximum selectable date
    showTime: false,                // Enable time selection
    timeFormat: '24',               // '12' or '24' hour format
    quickDates: true,               // Show quick date buttons
    theme: 'military'               // Theme (currently only 'military')
};
```

## CSS Classes

### Input Classes
- `.datepicker` - Basic date picker
- `.datetime-picker` - Date and time picker
- `.datepicker-input` - Styled input field

### Container Classes
- `.datepicker-container` - Main wrapper
- `.datepicker-dropdown` - Dropdown container
- `.datepicker-header` - Header section
- `.datepicker-body` - Body section
- `.datepicker-actions` - Action buttons

### State Classes
- `.today` - Today's date
- `.selected` - Selected date
- `.disabled` - Disabled date
- `.other-month` - Dates from other months

## Styling Customization

### Color Variables
```css
:root {
    --military-green: #3d5a40;
    --olive: #556b2f;
    --military-dark: #2d4a30;
    --military-light: #4a5f2a;
}
```

### Custom Styling
```css
/* Override default colors */
.datepicker-input {
    border-color: #your-color;
}

.datepicker-btn-primary {
    background: linear-gradient(135deg, #your-color1 0%, #your-color2 100%);
}
```

## Events

### Available Events
```javascript
// Date selection
datePicker.on('select', function(date) {
    console.log('Date selected:', date);
});

// Date change
datePicker.on('change', function(date) {
    console.log('Date changed:', date);
});

// Open/Close
datePicker.on('open', function() {
    console.log('Date picker opened');
});

datePicker.on('close', function() {
    console.log('Date picker closed');
});
```

## Integration Examples

### Profile Edit Form
```html
<div class="mb-3">
    <label class="form-label">Date of Birth</label>
    {{ form.date_of_birth|add_class:"form-control datepicker" }}
</div>
```

### Event Scheduling
```html
<div class="mb-3">
    <label class="form-label">Event Date & Time</label>
    <input type="datetime-local" class="form-control datetime-picker" name="event_datetime">
</div>
```

### Date Range Selection
```html
<div class="row">
    <div class="col-md-6">
        <label class="form-label">Start Date</label>
        <input type="date" class="form-control datepicker" name="start_date">
    </div>
    <div class="col-md-6">
        <label class="form-label">End Date</label>
        <input type="date" class="form-control datepicker" name="end_date">
    </div>
</div>
```

## Browser Support
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance
- **Lightweight**: ~15KB minified CSS + JS
- **Fast Rendering**: Optimized DOM manipulation
- **Memory Efficient**: Proper cleanup and event handling
- **Lazy Loading**: Only initializes when needed

## Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Screen Readers**: ARIA labels and descriptions
- **High Contrast**: Meets WCAG guidelines
- **Focus Management**: Proper focus handling

## Troubleshooting

### Common Issues
1. **Date picker not showing**: Ensure CSS and JS files are loaded
2. **Styling issues**: Check for CSS conflicts
3. **Form validation**: Ensure proper form field types

### Debug Mode
```javascript
// Enable debug mode
window.DatePickerDebug = true;
```

## Demo
Visit `/datepicker-demo/` to see the date picker in action with various examples and test cases.

## Support
For issues or questions, check the console for error messages or contact the development team.
