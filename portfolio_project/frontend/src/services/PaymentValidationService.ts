// Payment Validation Service following SOLID principles
// Single Responsibility: Handles all payment-related validations
// Open/Closed: Extensible for new validation rules
// Interface Segregation: Separate interfaces for different validation concerns
// Dependency Inversion: Depends on validation abstractions

export interface ValidationRule<T> {
  validate(value: T): ValidationResult;
  getMessage(): string;
}

export interface ValidationResult {
  isValid: boolean;
  message?: string;
  code?: string;
}

export interface PaymentFormData {
  email: string;
  user_name?: string;
  user_phone?: string;
  experience_level?: string;
  motivation?: string;
  message?: string;
  preferred_contact_method?: string;
  [key: string]: any;
}

export interface PaymentItem {
  id: number;
  title?: string;
  name?: string;
  price: number;
  price_display: string;
  currency?: string;
}

export interface PaymentValidationContext {
  item: PaymentItem;
  itemType: 'course' | 'workshop' | 'service';
  formData: PaymentFormData;
  user?: any;
}

// Email validation rule
export class EmailValidationRule implements ValidationRule<string> {
  validate(email: string): ValidationResult {
    if (!email || email.trim().length === 0) {
      return {
        isValid: false,
        message: 'Email is required',
        code: 'EMAIL_REQUIRED'
      };
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      return {
        isValid: false,
        message: 'Please enter a valid email address',
        code: 'EMAIL_INVALID'
      };
    }

    return { isValid: true };
  }

  getMessage(): string {
    return 'Valid email address is required';
  }
}

// Name validation rule
export class NameValidationRule implements ValidationRule<string> {
  private minLength: number;

  constructor(minLength: number = 2) {
    this.minLength = minLength;
  }

  validate(name: string): ValidationResult {
    if (!name || name.trim().length === 0) {
      return {
        isValid: false,
        message: 'Name is required',
        code: 'NAME_REQUIRED'
      };
    }

    if (name.trim().length < this.minLength) {
      return {
        isValid: false,
        message: `Name must be at least ${this.minLength} characters long`,
        code: 'NAME_TOO_SHORT'
      };
    }

    // Check for valid characters (letters, spaces, hyphens, apostrophes)
    const nameRegex = /^[a-zA-Z\s\-'\.]+$/;
    if (!nameRegex.test(name.trim())) {
      return {
        isValid: false,
        message: 'Name can only contain letters, spaces, hyphens, and apostrophes',
        code: 'NAME_INVALID_CHARACTERS'
      };
    }

    return { isValid: true };
  }

  getMessage(): string {
    return `Name must be at least ${this.minLength} characters long`;
  }
}

// Phone validation rule
export class PhoneValidationRule implements ValidationRule<string> {
  private required: boolean;

  constructor(required: boolean = false) {
    this.required = required;
  }

  validate(phone: string): ValidationResult {
    if (!phone || phone.trim().length === 0) {
      if (this.required) {
        return {
          isValid: false,
          message: 'Phone number is required',
          code: 'PHONE_REQUIRED'
        };
      }
      return { isValid: true }; // Optional field
    }

    // Remove all non-digit characters for validation
    const digitsOnly = phone.replace(/\D/g, '');
    
    // Check for minimum length (10 digits for most countries)
    if (digitsOnly.length < 10) {
      return {
        isValid: false,
        message: 'Phone number must be at least 10 digits',
        code: 'PHONE_TOO_SHORT'
      };
    }

    // Check for maximum length (15 digits as per international standard)
    if (digitsOnly.length > 15) {
      return {
        isValid: false,
        message: 'Phone number cannot exceed 15 digits',
        code: 'PHONE_TOO_LONG'
      };
    }

    return { isValid: true };
  }

  getMessage(): string {
    return this.required ? 'Valid phone number is required' : 'Valid phone number (optional)';
  }
}

// Item validation rule
export class ItemValidationRule implements ValidationRule<PaymentItem> {
  validate(item: PaymentItem): ValidationResult {
    if (!item) {
      return {
        isValid: false,
        message: 'Payment item is required',
        code: 'ITEM_REQUIRED'
      };
    }

    if (!item.id || item.id <= 0) {
      return {
        isValid: false,
        message: 'Invalid item ID',
        code: 'ITEM_ID_INVALID'
      };
    }

    if (!item.price || item.price <= 0) {
      return {
        isValid: false,
        message: 'Invalid item price',
        code: 'ITEM_PRICE_INVALID'
      };
    }

    if (!item.price_display || item.price_display.trim().length === 0) {
      return {
        isValid: false,
        message: 'Item price display is required',
        code: 'ITEM_PRICE_DISPLAY_REQUIRED'
      };
    }

    const title = item.title || item.name;
    if (!title || title.trim().length === 0) {
      return {
        isValid: false,
        message: 'Item title is required',
        code: 'ITEM_TITLE_REQUIRED'
      };
    }

    return { isValid: true };
  }

  getMessage(): string {
    return 'Valid payment item is required';
  }
}

// Experience level validation rule (for workshops)
export class ExperienceLevelValidationRule implements ValidationRule<string> {
  private validLevels = ['beginner', 'intermediate', 'advanced'];

  validate(level: string): ValidationResult {
    if (!level || level.trim().length === 0) {
      return {
        isValid: false,
        message: 'Experience level is required',
        code: 'EXPERIENCE_LEVEL_REQUIRED'
      };
    }

    if (!this.validLevels.includes(level.toLowerCase())) {
      return {
        isValid: false,
        message: 'Please select a valid experience level',
        code: 'EXPERIENCE_LEVEL_INVALID'
      };
    }

    return { isValid: true };
  }

  getMessage(): string {
    return 'Valid experience level is required';
  }
}

// Text length validation rule
export class TextLengthValidationRule implements ValidationRule<string> {
  private minLength: number;
  private maxLength: number;
  private required: boolean;

  constructor(minLength: number = 0, maxLength: number = 1000, required: boolean = false) {
    this.minLength = minLength;
    this.maxLength = maxLength;
    this.required = required;
  }

  validate(text: string): ValidationResult {
    if (!text || text.trim().length === 0) {
      if (this.required) {
        return {
          isValid: false,
          message: 'This field is required',
          code: 'TEXT_REQUIRED'
        };
      }
      return { isValid: true }; // Optional field
    }

    const trimmedText = text.trim();

    if (trimmedText.length < this.minLength) {
      return {
        isValid: false,
        message: `Text must be at least ${this.minLength} characters long`,
        code: 'TEXT_TOO_SHORT'
      };
    }

    if (trimmedText.length > this.maxLength) {
      return {
        isValid: false,
        message: `Text cannot exceed ${this.maxLength} characters`,
        code: 'TEXT_TOO_LONG'
      };
    }

    return { isValid: true };
  }

  getMessage(): string {
    if (this.required) {
      return `Required text (${this.minLength}-${this.maxLength} characters)`;
    }
    return `Optional text (max ${this.maxLength} characters)`;
  }
}

// Main validation service
export class PaymentValidationService {
  private static instance: PaymentValidationService;

  private constructor() {}

  public static getInstance(): PaymentValidationService {
    if (!PaymentValidationService.instance) {
      PaymentValidationService.instance = new PaymentValidationService();
    }
    return PaymentValidationService.instance;
  }

  // Validate complete payment context
  public validatePaymentContext(context: PaymentValidationContext): ValidationResult {
    const errors: string[] = [];

    // Validate item
    const itemValidation = this.validateItem(context.item);
    if (!itemValidation.isValid) {
      errors.push(itemValidation.message || 'Invalid item');
    }

    // Validate item type
    const itemTypeValidation = this.validateItemType(context.itemType);
    if (!itemTypeValidation.isValid) {
      errors.push(itemTypeValidation.message || 'Invalid item type');
    }

    // Validate form data based on item type
    const formValidation = this.validateFormData(context.formData, context.itemType);
    if (!formValidation.isValid) {
      errors.push(formValidation.message || 'Invalid form data');
    }

    return {
      isValid: errors.length === 0,
      message: errors.length > 0 ? errors.join('; ') : undefined,
      code: errors.length > 0 ? 'VALIDATION_FAILED' : undefined
    };
  }

  // Validate payment item
  public validateItem(item: PaymentItem): ValidationResult {
    const rule = new ItemValidationRule();
    return rule.validate(item);
  }

  // Validate item type
  public validateItemType(itemType: string): ValidationResult {
    const validTypes = ['course', 'workshop', 'service'];
    
    if (!itemType || !validTypes.includes(itemType)) {
      return {
        isValid: false,
        message: 'Invalid item type. Must be course, workshop, or service',
        code: 'ITEM_TYPE_INVALID'
      };
    }

    return { isValid: true };
  }

  // Validate form data based on item type
  public validateFormData(formData: PaymentFormData, itemType: string): ValidationResult {
    const errors: string[] = [];

    // Email is always required
    const emailRule = new EmailValidationRule();
    const emailValidation = emailRule.validate(formData.email);
    if (!emailValidation.isValid) {
      errors.push(emailValidation.message || 'Invalid email');
    }

    // Name validation for workshops and services
    if (itemType === 'workshop' || itemType === 'service') {
      const nameRule = new NameValidationRule(2);
      const nameValidation = nameRule.validate(formData.user_name || '');
      if (!nameValidation.isValid) {
        errors.push(nameValidation.message || 'Invalid name');
      }

      // Phone validation (optional for most cases)
      const phoneRule = new PhoneValidationRule(false);
      const phoneValidation = phoneRule.validate(formData.user_phone || '');
      if (!phoneValidation.isValid) {
        errors.push(phoneValidation.message || 'Invalid phone number');
      }
    }

    // Workshop-specific validations
    if (itemType === 'workshop') {
      // Experience level is required for workshops
      const experienceRule = new ExperienceLevelValidationRule();
      const experienceValidation = experienceRule.validate(formData.experience_level || '');
      if (!experienceValidation.isValid) {
        errors.push(experienceValidation.message || 'Invalid experience level');
      }

      // Motivation is optional but has length limits
      const motivationRule = new TextLengthValidationRule(0, 500, false);
      const motivationValidation = motivationRule.validate(formData.motivation || '');
      if (!motivationValidation.isValid) {
        errors.push(motivationValidation.message || 'Invalid motivation text');
      }
    }

    // Service-specific validations
    if (itemType === 'service') {
      // Message is optional but has length limits
      const messageRule = new TextLengthValidationRule(0, 1000, false);
      const messageValidation = messageRule.validate(formData.message || '');
      if (!messageValidation.isValid) {
        errors.push(messageValidation.message || 'Invalid message text');
      }

      // Preferred contact method validation
      const validContactMethods = ['whatsapp', 'call', 'email'];
      const contactMethod = formData.preferred_contact_method || 'whatsapp';
      if (!validContactMethods.includes(contactMethod)) {
        errors.push('Invalid preferred contact method');
      }
    }

    return {
      isValid: errors.length === 0,
      message: errors.length > 0 ? errors.join('; ') : undefined,
      code: errors.length > 0 ? 'FORM_VALIDATION_FAILED' : undefined
    };
  }

  // Validate individual field
  public validateField(fieldName: string, value: any, context: PaymentValidationContext): ValidationResult {
    switch (fieldName) {
      case 'email':
        return new EmailValidationRule().validate(value);
      
      case 'user_name':
        return new NameValidationRule(2).validate(value);
      
      case 'user_phone':
        return new PhoneValidationRule(false).validate(value);
      
      case 'experience_level':
        return new ExperienceLevelValidationRule().validate(value);
      
      case 'motivation':
        return new TextLengthValidationRule(0, 500, false).validate(value);
      
      case 'message':
        return new TextLengthValidationRule(0, 1000, false).validate(value);
      
      default:
        return { isValid: true }; // Unknown fields are considered valid
    }
  }

  // Get validation requirements for a field
  public getFieldRequirements(fieldName: string, itemType: string): string {
    switch (fieldName) {
      case 'email':
        return 'Valid email address is required';
      
      case 'user_name':
        if (itemType === 'workshop' || itemType === 'service') {
          return 'Full name is required (minimum 2 characters)';
        }
        return 'Full name (optional)';
      
      case 'user_phone':
        return 'Phone number (optional, 10-15 digits)';
      
      case 'experience_level':
        if (itemType === 'workshop') {
          return 'Experience level is required';
        }
        return 'Experience level (optional)';
      
      case 'motivation':
        return 'Motivation (optional, max 500 characters)';
      
      case 'message':
        return 'Message (optional, max 1000 characters)';
      
      case 'preferred_contact_method':
        return 'Preferred contact method';
      
      default:
        return 'Field requirements not specified';
    }
  }
}

// Export singleton instance
export const paymentValidationService = PaymentValidationService.getInstance();

// Utility functions for common validation patterns
export const ValidationUtils = {
  // Validate email
  validateEmail: (email: string) => {
    return new EmailValidationRule().validate(email);
  },

  // Validate name
  validateName: (name: string, required: boolean = true) => {
    if (!required && (!name || name.trim().length === 0)) {
      return { isValid: true };
    }
    return new NameValidationRule(2).validate(name);
  },

  // Validate phone
  validatePhone: (phone: string, required: boolean = false) => {
    return new PhoneValidationRule(required).validate(phone);
  },

  // Validate payment context
  validatePaymentContext: (context: PaymentValidationContext) => {
    return paymentValidationService.validatePaymentContext(context);
  },

  // Get field requirements
  getFieldRequirements: (fieldName: string, itemType: string) => {
    return paymentValidationService.getFieldRequirements(fieldName, itemType);
  }
};