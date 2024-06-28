odoo.define('bloopark_realestatex_complaints.complaint_form_validate', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.ComplaintForm = publicWidget.Widget.extend({
        selector: "#complaint_form_container form",
        events: {
            'submit': "_onSubmitButton",
        },
        start: function () {
            // Call the parent method
            this._super.apply(this, arguments);

            // Reset the form to its default state
            this.$el[0].reset();
        },
        _get_fields_rules: function () {
            // Define form fields and their validation rules
            return [
                {
                    element: this.$el.find('input[name="title"]'),
                    validate: function(value) { return value.trim() !== ''; },
                    errorMessage: 'Please enter your title.'
                },
                {
                    element: this.$el.find('input[name="email"]'),
                    validate: function(value) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim()); },
                    errorMessage: 'Please enter a valid email address.'
                },
                {
                    element: this.$el.find('input[name="address"]'),
                    validate: function(value) { return value.trim() !== ''; },
                    errorMessage: 'Please enter your address.'
                },
                {
                    element: this.$el.find('select[name="type"]'),
                    validate: function(value) {
                        return ['question', 'electrical', 'heating', 'other'].includes(value);
                    },
                    errorMessage: 'Please select a valid complaint type.'
                },
                {
                    element: this.$el.find('textarea[name="description"]'),
                    validate: function(value) { return value.trim() !== ''; },
                    errorMessage: 'Please enter a description.'
                }
            ];    
        },
        
        _onSubmitButton: function (ev) {
            ev.preventDefault(); // Prevent the default form submission
            const fields = this._get_fields_rules()
            // Validation status
            let isValid = true;

            // Loop through fields and validate
            fields.forEach(function(field) {
                let value = field.element.val();
                let feedback = field.element.next('.invalid-feedback');

                // Create feedback element if it doesn't exist
                if (feedback.length === 0) {
                    feedback = $('<div class="invalid-feedback"></div>');
                    field.element.after(feedback);
                }

                if (!field.validate(value)) {
                    isValid = false;
                    field.element.addClass('is-invalid');
                    feedback.text(field.errorMessage).show();
                } else {
                    field.element.removeClass('is-invalid');
                    feedback.hide();
                }
            });

            // If the form is valid, submit it
            if (isValid) {
                this.$el.off('submit').submit(); // Remove the event listener to avoid infinite loop and submit the form
            }
        },
    });
});
