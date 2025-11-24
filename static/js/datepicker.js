/**
 * Custom Date Picker - Military Theme
 * Advanced date picker with beautiful UI and military styling
 */
class MilitaryDatePicker {
    constructor(input, options = {}) {
        this.input = input;
        this.options = {
            format: 'yyyy-mm-dd',
            minDate: null,
            maxDate: null,
            showTime: false,
            timeFormat: '24',
            quickDates: true,
            theme: 'military',
            ...options
        };
        
        this.isOpen = false;
        this.selectedDate = null;
        this.currentMonth = new Date().getMonth();
        this.currentYear = new Date().getFullYear();
        
        this.init();
    }
    
    init() {
        this.createContainer();
        this.bindEvents();
        this.setInitialValue();
    }
    
    createContainer() {
        // Create wrapper
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'datepicker-container';
        
        // Wrap input
        this.input.parentNode.insertBefore(this.wrapper, this.input);
        this.wrapper.appendChild(this.input);
        
        // Add calendar icon
        this.icon = document.createElement('i');
        this.icon.className = 'fas fa-calendar-alt datepicker-icon';
        this.wrapper.appendChild(this.icon);
        
        // Create dropdown
        this.dropdown = document.createElement('div');
        this.dropdown.className = 'datepicker-dropdown';
        this.dropdown.style.display = 'none';
        this.wrapper.appendChild(this.dropdown);
        
        this.render();
    }
    
    render() {
        const date = new Date(this.currentYear, this.currentMonth, 1);
        const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0).getDate();
        const firstDayOfWeek = date.getDay();
        
        this.dropdown.innerHTML = `
            <div class="datepicker-header">
                <h5 class="datepicker-title">Select Date</h5>
                <div class="datepicker-nav">
                    <button class="datepicker-nav-btn" data-action="prev-year">
                        <i class="fas fa-angle-double-left"></i>
                    </button>
                    <button class="datepicker-nav-btn" data-action="prev-month">
                        <i class="fas fa-angle-left"></i>
                    </button>
                    <button class="datepicker-nav-btn" data-action="next-month">
                        <i class="fas fa-angle-right"></i>
                    </button>
                    <button class="datepicker-nav-btn" data-action="next-year">
                        <i class="fas fa-angle-double-right"></i>
                    </button>
                </div>
            </div>
            
            <div class="datepicker-body">
                <div class="datepicker-month-year">
                    <select class="datepicker-month-select">
                        ${this.getMonthOptions()}
                    </select>
                    <select class="datepicker-year-select">
                        ${this.getYearOptions()}
                    </select>
                </div>
                
                <table class="datepicker-calendar">
                    <thead>
                        <tr>
                            <th>Sun</th>
                            <th>Mon</th>
                            <th>Tue</th>
                            <th>Wed</th>
                            <th>Thu</th>
                            <th>Fri</th>
                            <th>Sat</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.generateCalendarGrid(firstDayOfWeek, lastDay)}
                    </tbody>
                </table>
                
                ${this.options.quickDates ? this.getQuickDatesHTML() : ''}
                
                ${this.options.showTime ? this.getTimePickerHTML() : ''}
            </div>
            
            <div class="datepicker-actions">
                <button class="datepicker-btn datepicker-btn-secondary" data-action="clear">
                    <i class="fas fa-times me-2"></i>Clear
                </button>
                <button class="datepicker-btn datepicker-btn-primary" data-action="today">
                    <i class="fas fa-calendar-day me-2"></i>Today
                </button>
                <button class="datepicker-btn datepicker-btn-primary" data-action="apply">
                    <i class="fas fa-check me-2"></i>Apply
                </button>
            </div>
        `;
    }
    
    generateCalendarGrid(firstDayOfWeek, lastDay) {
        let html = '';
        let day = 1;
        const today = new Date();
        const isToday = (dayNum) => {
            return dayNum === today.getDate() && 
                   this.currentMonth === today.getMonth() && 
                   this.currentYear === today.getFullYear();
        };
        
        const isSelected = (dayNum) => {
            if (!this.selectedDate) return false;
            return dayNum === this.selectedDate.getDate() && 
                   this.currentMonth === this.selectedDate.getMonth() && 
                   this.currentYear === this.selectedDate.getFullYear();
        };
        
        const isDisabled = (dayNum) => {
            const date = new Date(this.currentYear, this.currentMonth, dayNum);
            if (this.options.minDate && date < this.options.minDate) return true;
            if (this.options.maxDate && date > this.options.maxDate) return true;
            return false;
        };
        
        for (let week = 0; week < 6; week++) {
            html += '<tr>';
            for (let dayOfWeek = 0; dayOfWeek < 7; dayOfWeek++) {
                if (week === 0 && dayOfWeek < firstDayOfWeek) {
                    // Previous month days
                    const prevMonth = new Date(this.currentYear, this.currentMonth - 1, 0);
                    const prevDay = prevMonth.getDate() - (firstDayOfWeek - dayOfWeek - 1);
                    html += `<td class="other-month">${prevDay}</td>`;
                } else if (day > lastDay) {
                    // Next month days
                    const nextDay = day - lastDay;
                    html += `<td class="other-month">${nextDay}</td>`;
                    day++;
                } else {
                    const classes = [];
                    if (isToday(day)) classes.push('today');
                    if (isSelected(day)) classes.push('selected');
                    if (isDisabled(day)) classes.push('disabled');
                    
                    html += `<td class="${classes.join(' ')}" data-day="${day}">${day}</td>`;
                    day++;
                }
            }
            html += '</tr>';
            if (day > lastDay) break;
        }
        
        return html;
    }
    
    getMonthOptions() {
        const months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        
        return months.map((month, index) => 
            `<option value="${index}" ${index === this.currentMonth ? 'selected' : ''}>${month}</option>`
        ).join('');
    }
    
    getYearOptions() {
        const currentYear = new Date().getFullYear();
        const years = [];
        
        for (let year = currentYear - 50; year <= currentYear + 10; year++) {
            years.push(`<option value="${year}" ${year === this.currentYear ? 'selected' : ''}>${year}</option>`);
        }
        
        return years.join('');
    }
    
    getQuickDatesHTML() {
        return `
            <div class="datepicker-quick-dates">
                <h6>Quick Select</h6>
                <div class="datepicker-quick-buttons">
                    <button class="datepicker-quick-btn" data-action="today">Today</button>
                    <button class="datepicker-quick-btn" data-action="tomorrow">Tomorrow</button>
                    <button class="datepicker-quick-btn" data-action="next-week">Next Week</button>
                    <button class="datepicker-quick-btn" data-action="next-month">Next Month</button>
                    <button class="datepicker-quick-btn" data-action="next-year">Next Year</button>
                </div>
            </div>
        `;
    }
    
    getTimePickerHTML() {
        return `
            <div class="datepicker-time">
                <label class="datepicker-time-label">Time</label>
                <div class="datepicker-time-inputs">
                    <input type="number" class="datepicker-time-input" min="0" max="23" placeholder="HH" data-time="hours">
                    <span>:</span>
                    <input type="number" class="datepicker-time-input" min="0" max="59" placeholder="MM" data-time="minutes">
                    ${this.options.timeFormat === '12' ? `
                        <select class="datepicker-time-input" data-time="ampm">
                            <option value="AM">AM</option>
                            <option value="PM">PM</option>
                        </select>
                    ` : ''}
                </div>
            </div>
        `;
    }
    
    bindEvents() {
        // Toggle dropdown
        this.icon.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggle();
        });
        
        this.input.addEventListener('click', (e) => {
            e.stopPropagation();
            this.open();
        });
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.wrapper.contains(e.target)) {
                this.close();
            }
        });
        
        // Dropdown events
        this.dropdown.addEventListener('click', (e) => {
            e.stopPropagation();
            this.handleDropdownClick(e);
        });
        
        // Input change
        this.input.addEventListener('change', () => {
            this.parseInputValue();
        });
    }
    
    handleDropdownClick(e) {
        const action = e.target.closest('[data-action]')?.dataset.action;
        const day = e.target.closest('[data-day]')?.dataset.day;
        
        if (day && !e.target.classList.contains('disabled')) {
            this.selectDate(parseInt(day));
        } else if (action) {
            this.handleAction(action);
        }
    }
    
    handleAction(action) {
        const today = new Date();
        
        switch (action) {
            case 'prev-year':
                this.currentYear--;
                this.render();
                break;
            case 'next-year':
                this.currentYear++;
                this.render();
                break;
            case 'prev-month':
                this.currentMonth--;
                if (this.currentMonth < 0) {
                    this.currentMonth = 11;
                    this.currentYear--;
                }
                this.render();
                break;
            case 'next-month':
                this.currentMonth++;
                if (this.currentMonth > 11) {
                    this.currentMonth = 0;
                    this.currentYear++;
                }
                this.render();
                break;
            case 'today':
                this.selectDate(today.getDate());
                this.apply();
                break;
            case 'tomorrow':
                const tomorrow = new Date(today);
                tomorrow.setDate(today.getDate() + 1);
                this.setDate(tomorrow);
                this.apply();
                break;
            case 'next-week':
                const nextWeek = new Date(today);
                nextWeek.setDate(today.getDate() + 7);
                this.setDate(nextWeek);
                this.apply();
                break;
            case 'next-month':
                const nextMonth = new Date(today);
                nextMonth.setMonth(today.getMonth() + 1);
                this.setDate(nextMonth);
                this.apply();
                break;
            case 'next-year':
                const nextYear = new Date(today);
                nextYear.setFullYear(today.getFullYear() + 1);
                this.setDate(nextYear);
                this.apply();
                break;
            case 'clear':
                this.clear();
                break;
            case 'apply':
                this.apply();
                break;
        }
    }
    
    selectDate(day) {
        this.selectedDate = new Date(this.currentYear, this.currentMonth, day);
        this.render();
        
        // Add selection animation
        const cell = this.dropdown.querySelector(`[data-day="${day}"]`);
        if (cell) {
            cell.classList.add('selecting');
            setTimeout(() => cell.classList.remove('selecting'), 300);
        }
    }
    
    setDate(date) {
        this.selectedDate = new Date(date);
        this.currentMonth = date.getMonth();
        this.currentYear = date.getFullYear();
        this.render();
    }
    
    apply() {
        if (this.selectedDate) {
            this.input.value = this.formatDate(this.selectedDate);
            this.input.dispatchEvent(new Event('change', { bubbles: true }));
        }
        this.close();
    }
    
    clear() {
        this.selectedDate = null;
        this.input.value = '';
        this.input.dispatchEvent(new Event('change', { bubbles: true }));
        this.close();
    }
    
    toggle() {
        this.isOpen ? this.close() : this.open();
    }
    
    open() {
        this.isOpen = true;
        this.dropdown.style.display = 'block';
        this.render();
    }
    
    close() {
        this.isOpen = false;
        this.dropdown.style.display = 'none';
    }
    
    formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        
        if (this.options.showTime) {
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            return `${year}-${month}-${day} ${hours}:${minutes}`;
        }
        
        return `${year}-${month}-${day}`;
    }
    
    parseInputValue() {
        const value = this.input.value;
        if (value) {
            const date = new Date(value);
            if (!isNaN(date.getTime())) {
                this.setDate(date);
            }
        }
    }
    
    setInitialValue() {
        if (this.input.value) {
            this.parseInputValue();
        }
    }
}

// Auto-initialize date pickers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all date inputs
    const dateInputs = document.querySelectorAll('input[type="date"], input.datepicker');
    dateInputs.forEach(input => {
        // Convert to text input for better control
        input.type = 'text';
        input.classList.add('datepicker-input');
        
        // Initialize date picker
        new MilitaryDatePicker(input, {
            format: 'yyyy-mm-dd',
            showTime: input.classList.contains('datetime-picker'),
            quickDates: true
        });
    });
    
    // Initialize datetime inputs
    const datetimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    datetimeInputs.forEach(input => {
        input.type = 'text';
        input.classList.add('datepicker-input', 'datetime-picker');
        
        new MilitaryDatePicker(input, {
            format: 'yyyy-mm-dd HH:mm',
            showTime: true,
            timeFormat: '24',
            quickDates: true
        });
    });
});

// Export for manual initialization
window.MilitaryDatePicker = MilitaryDatePicker;
