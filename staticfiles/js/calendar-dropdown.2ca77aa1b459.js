/**
 * Calendar Dropdown - Military Theme
 * Beautiful calendar-style dropdowns for month and year selection
 */
class CalendarDropdown {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            type: 'month', // 'month' or 'year'
            placeholder: 'Select...',
            ...options
        };
        
        this.isOpen = false;
        this.selectedValue = null;
        this.selectedText = null;
        
        this.init();
    }
    
    init() {
        this.createDropdown();
        this.bindEvents();
        this.setInitialValue();
    }
    
    createDropdown() {
        // Create wrapper
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'calendar-dropdown';
        
        // Wrap original element
        this.element.parentNode.insertBefore(this.wrapper, this.element);
        this.wrapper.appendChild(this.element);
        
        // Hide original element
        this.element.style.display = 'none';
        
        // Create toggle button
        this.toggle = document.createElement('button');
        this.toggle.className = 'calendar-dropdown-toggle';
        this.toggle.type = 'button';
        this.toggle.innerHTML = `
            <span class="calendar-dropdown-text calendar-dropdown-placeholder">${this.options.placeholder}</span>
            <i class="fas fa-chevron-down calendar-dropdown-icon"></i>
        `;
        this.wrapper.appendChild(this.toggle);
        
        // Create dropdown menu
        this.menu = document.createElement('div');
        this.menu.className = 'calendar-dropdown-menu';
        this.menu.style.display = 'none';
        this.wrapper.appendChild(this.menu);
        
        this.render();
    }
    
    render() {
        if (this.options.type === 'month') {
            this.renderMonthDropdown();
        } else if (this.options.type === 'year') {
            this.renderYearDropdown();
        }
    }
    
    renderMonthDropdown() {
        const months = [
            { value: '01', text: 'January', short: 'Jan' },
            { value: '02', text: 'February', short: 'Feb' },
            { value: '03', text: 'March', short: 'Mar' },
            { value: '04', text: 'April', short: 'Apr' },
            { value: '05', text: 'May', short: 'May' },
            { value: '06', text: 'June', short: 'Jun' },
            { value: '07', text: 'July', short: 'Jul' },
            { value: '08', text: 'August', short: 'Aug' },
            { value: '09', text: 'September', short: 'Sep' },
            { value: '10', text: 'October', short: 'Oct' },
            { value: '11', text: 'November', short: 'Nov' },
            { value: '12', text: 'December', short: 'Dec' }
        ];
        
        this.menu.innerHTML = `
            <div class="calendar-dropdown-header">
                <i class="fas fa-calendar-alt me-2"></i>Select Month
            </div>
            <div class="calendar-dropdown-body">
                <div class="calendar-month-grid">
                    ${months.map(month => `
                        <div class="calendar-month-item" data-value="${month.value}" data-text="${month.text}">
                            ${month.short}
                        </div>
                    `).join('')}
                </div>
                <div class="calendar-quick-select">
                    <h6>Quick Select</h6>
                    <div class="calendar-quick-buttons">
                        <button class="calendar-quick-btn" data-action="current">Current Month</button>
                        <button class="calendar-quick-btn" data-action="next">Next Month</button>
                    </div>
                </div>
            </div>
            <div class="calendar-dropdown-actions">
                <button class="calendar-dropdown-btn calendar-dropdown-btn-secondary" data-action="clear">
                    <i class="fas fa-times me-2"></i>Clear
                </button>
                <button class="calendar-dropdown-btn calendar-dropdown-btn-primary" data-action="apply">
                    <i class="fas fa-check me-2"></i>Apply
                </button>
            </div>
        `;
    }
    
    renderYearDropdown() {
        const currentYear = new Date().getFullYear();
        const years = [];
        
        // Generate years from current year to 10 years ahead
        for (let year = currentYear; year <= currentYear + 10; year++) {
            years.push({
                value: year.toString(),
                text: year.toString()
            });
        }
        
        this.menu.innerHTML = `
            <div class="calendar-dropdown-header">
                <i class="fas fa-calendar-alt me-2"></i>Select Year
            </div>
            <div class="calendar-dropdown-body">
                <div class="calendar-year-grid">
                    ${years.map(year => `
                        <div class="calendar-year-item" data-value="${year.value}" data-text="${year.text}">
                            ${year.text}
                        </div>
                    `).join('')}
                </div>
                <div class="calendar-quick-select">
                    <h6>Quick Select</h6>
                    <div class="calendar-quick-buttons">
                        <button class="calendar-quick-btn" data-action="current">Current Year</button>
                        <button class="calendar-quick-btn" data-action="next">Next Year</button>
                    </div>
                </div>
            </div>
            <div class="calendar-dropdown-actions">
                <button class="calendar-dropdown-btn calendar-dropdown-btn-secondary" data-action="clear">
                    <i class="fas fa-times me-2"></i>Clear
                </button>
                <button class="calendar-dropdown-btn calendar-dropdown-btn-primary" data-action="apply">
                    <i class="fas fa-check me-2"></i>Apply
                </button>
            </div>
        `;
    }
    
    bindEvents() {
        // Toggle dropdown
        this.toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggle();
        });
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.wrapper.contains(e.target)) {
                this.close();
            }
        });
        
        // Menu events
        this.menu.addEventListener('click', (e) => {
            e.stopPropagation();
            this.handleMenuClick(e);
        });
        
        // Original element change
        this.element.addEventListener('change', () => {
            this.updateFromOriginal();
        });
    }
    
    handleMenuClick(e) {
        const item = e.target.closest('.calendar-month-item, .calendar-year-item');
        const button = e.target.closest('.calendar-dropdown-btn, .calendar-quick-btn');
        
        if (item) {
            this.selectItem(item);
        } else if (button) {
            this.handleButtonClick(button);
        }
    }
    
    selectItem(item) {
        // Remove previous selection
        this.menu.querySelectorAll('.calendar-month-item, .calendar-year-item').forEach(el => {
            el.classList.remove('selected');
        });
        
        // Add selection to clicked item
        item.classList.add('selected');
        item.classList.add('selecting');
        
        // Store selected values
        this.selectedValue = item.dataset.value;
        this.selectedText = item.dataset.text;
        
        // Remove selecting class after animation
        setTimeout(() => {
            item.classList.remove('selecting');
        }, 300);
    }
    
    handleButtonClick(button) {
        const action = button.dataset.action;
        
        switch (action) {
            case 'clear':
                this.clear();
                break;
            case 'apply':
                this.apply();
                break;
            case 'current':
                this.selectCurrent();
                break;
            case 'next':
                this.selectNext();
                break;
        }
    }
    
    selectCurrent() {
        const now = new Date();
        
        if (this.options.type === 'month') {
            const monthValue = String(now.getMonth() + 1).padStart(2, '0');
            const monthItem = this.menu.querySelector(`[data-value="${monthValue}"]`);
            if (monthItem) {
                this.selectItem(monthItem);
            }
        } else if (this.options.type === 'year') {
            const yearValue = now.getFullYear().toString();
            const yearItem = this.menu.querySelector(`[data-value="${yearValue}"]`);
            if (yearItem) {
                this.selectItem(yearItem);
            }
        }
    }
    
    selectNext() {
        const now = new Date();
        
        if (this.options.type === 'month') {
            const nextMonth = now.getMonth() + 2; // +2 because getMonth() is 0-based
            const monthValue = String(nextMonth).padStart(2, '0');
            const monthItem = this.menu.querySelector(`[data-value="${monthValue}"]`);
            if (monthItem) {
                this.selectItem(monthItem);
            }
        } else if (this.options.type === 'year') {
            const nextYear = now.getFullYear() + 1;
            const yearValue = nextYear.toString();
            const yearItem = this.menu.querySelector(`[data-value="${yearValue}"]`);
            if (yearItem) {
                this.selectItem(yearItem);
            }
        }
    }
    
    apply() {
        if (this.selectedValue) {
            this.element.value = this.selectedValue;
            this.element.dispatchEvent(new Event('change', { bubbles: true }));
            
            // Update toggle text
            const textElement = this.toggle.querySelector('.calendar-dropdown-text');
            textElement.textContent = this.selectedText;
            textElement.classList.remove('calendar-dropdown-placeholder');
            textElement.classList.add('calendar-dropdown-text');
        }
        this.close();
    }
    
    clear() {
        this.selectedValue = null;
        this.selectedText = null;
        this.element.value = '';
        this.element.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Update toggle text
        const textElement = this.toggle.querySelector('.calendar-dropdown-text');
        textElement.textContent = this.options.placeholder;
        textElement.classList.add('calendar-dropdown-placeholder');
        textElement.classList.remove('calendar-dropdown-text');
        
        // Remove selections
        this.menu.querySelectorAll('.calendar-month-item, .calendar-year-item').forEach(el => {
            el.classList.remove('selected');
        });
        
        this.close();
    }
    
    toggle() {
        this.isOpen ? this.close() : this.open();
    }
    
    open() {
        this.isOpen = true;
        this.menu.style.display = 'block';
        this.toggle.classList.add('active');
    }
    
    close() {
        this.isOpen = false;
        this.menu.style.display = 'none';
        this.toggle.classList.remove('active');
    }
    
    updateFromOriginal() {
        const value = this.element.value;
        if (value) {
            const item = this.menu.querySelector(`[data-value="${value}"]`);
            if (item) {
                this.selectItem(item);
                this.apply();
            }
        }
    }
    
    setInitialValue() {
        if (this.element.value) {
            this.updateFromOriginal();
        }
    }
}

// Auto-initialize calendar dropdowns
document.addEventListener('DOMContentLoaded', function() {
    // Check if auto-initialization is disabled
    if (window.disableCalendarAutoInit) {
        console.log('Calendar dropdown auto-initialization disabled');
        return;
    }
    
    // Initialize month dropdowns
    const monthSelects = document.querySelectorAll('select[id*="exp-month"], select[id*="month"]');
    monthSelects.forEach(select => {
        if (!select.hasAttribute('data-calendar-initialized')) {
            new CalendarDropdown(select, {
                type: 'month',
                placeholder: 'Select Month'
            });
            select.setAttribute('data-calendar-initialized', 'true');
        }
    });
    
    // Initialize year dropdowns
    const yearSelects = document.querySelectorAll('select[id*="exp-year"], select[id*="year"]');
    yearSelects.forEach(select => {
        if (!select.hasAttribute('data-calendar-initialized')) {
            new CalendarDropdown(select, {
                type: 'year',
                placeholder: 'Select Year'
            });
            select.setAttribute('data-calendar-initialized', 'true');
        }
    });
});

// Export for manual initialization
window.CalendarDropdown = CalendarDropdown;
