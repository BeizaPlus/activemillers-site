import React, { useState } from 'react';

const EmailSignupForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage('');

    try
    {
      // Create a form element and submit it to avoid CORS issues
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = 'https://gem.godaddy.com/signups/subscribe/176cee535f3e46b081fddeedb369bf0e';
      form.target = '_blank';
      form.style.display = 'none';

      // Add form fields
      const fields = {
        'utf8': '✓',
        'authenticity_token': '7HEm8ZtK1q7UX8ZmCJZcMEDMIT7GJ2VtZ3BFpjwbn8uDuUDjedilW_uZAOjp3wVGNKViMXJiQZ9pl-N7vX2VaQ',
        'signup[email]': email,
        'db8feace51f8c2719eb409586b109917': '', // honeypot
        'beacon': 'on'
      };

      Object.entries(fields).forEach(([name, value]) => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = value;
        form.appendChild(input);
      });

      // Add form to DOM, submit, and remove
      document.body.appendChild(form);
      form.submit();
      document.body.removeChild(form);

      // Show success message
      setMessage('Thank you! Check your email for the download link.');
      setEmail('');

    } catch (error)
    {
      console.error('Form submission error:', error);
      setMessage('Something went wrong. Please try again.');
    } finally
    {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="am-lead-wrap">
      <form onSubmit={handleSubmit} className="space-y-4 text-center">
        <div className="mimi_field required">
          <label htmlFor="signup_email" className="form-label text-center">
            Email*
          </label>
          <input
            id="signup_email"
            name="signup[email]"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            autoComplete="email"
            required
            className="form-input text-center"
          />
        </div>

        {/* Honeypot fields */}
        <div style={{ background: '#fff', fontSize: '1px', height: 0, overflow: 'hidden' }}>
          <input
            type="text"
            name="db8feace51f8c2719eb409586b109917"
            style={{ fontSize: '1px', width: '1px!important', height: '1px!important', border: '0!important', lineHeight: '1px!important', padding: 0, minHeight: '1px!important' }}
          />
          <input className="checkbox" type="checkbox" name="beacon" />
        </div>

        <div className="mimi_field flex justify-center">
          <button
            type="submit"
            className="btn-primary"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Sending...' : 'Download Free ePub'}
          </button>
        </div>

        {message && (
          <div className={`text-center text-sm ${message.includes('Thank you') ? 'text-green-600' : 'text-red-600'}`}>
            {message}
          </div>
        )}
      </form>
    </div>
  );
};

export default EmailSignupForm;
