'use strict';
// A deliberate, user-controlled illustration. No autoplay, timers, or tracking.
const nextStep = document.querySelector('#demo-next');
if (nextStep) {
  const states = [
    { player: [1, 1], echo: null, open: false, caption: 'First, walk to the switch.' },
    { player: [1, 1], echo: [4, 1], open: true, caption: 'Rewind. Your echo repeats the route and holds the switch.' },
    { player: [7, 3], echo: [4, 1], open: true, caption: 'With the door open, your present self reaches the exit.' },
  ];
  let step = 0;
  const caption = document.querySelector('#demo-caption');
  caption.setAttribute('aria-live', 'polite');
  function position(selector, coordinates) {
    const actor = document.querySelector(selector);
    actor.style.opacity = coordinates ? '1' : '0';
    if (coordinates) {
      actor.style.left = `${1.7 + coordinates[0] * 11.2}%`;
      actor.style.top = `${5.6 + coordinates[1] * 20.4}%`;
    }
  }
  nextStep.addEventListener('click', () => {
    step = (step + 1) % states.length;
    const state = states[step];
    position('.player', state.player);
    position('.echo', state.echo);
    document.querySelector('.door').classList.toggle('open', state.open);
    document.querySelector('.step-counter').textContent = `0${step + 1} / 03`;
    caption.textContent = state.caption;
    nextStep.setAttribute('aria-label', step === 2 ? 'Restart the gameplay preview' : 'Show the next step of the gameplay preview');
  });
}

const form = document.querySelector('#support-form');
if (form) {
  const status = document.querySelector('#form-status');
  const topic = document.querySelector('#topic');
  const device = document.querySelector('#device');
  const message = document.querySelector('#message');
  function body() {
    return `${topic.value}\n\nDevice & app version: ${device.value.trim() || 'Not specified'}\n\n${message.value.trim()}`;
  }
  function validate() {
    message.setCustomValidity(message.value.trim().length < 10 ? 'Please include at least 10 characters so we can help.' : '');
    return form.reportValidity();
  }
  message.addEventListener('input', () => message.setCustomValidity(''));
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!validate()) return;
    const url = `mailto:lamnv260398@gmail.com?subject=${encodeURIComponent(`Time Echo — ${topic.value}`)}&body=${encodeURIComponent(body())}`;
    const draft = document.querySelector('#email-draft');
    draft.href = url;
    draft.hidden = false;
    status.textContent = 'Your draft is ready. Open it below, then send it from your email app. If no email app opens, copy the message and email lamnv260398@gmail.com.';
  });
  // Invalidate the prepared draft when fields change; never send stale content.
  form.addEventListener('input', () => {
    document.querySelector('#email-draft').hidden = true;
    status.textContent = '';
  });
  document.querySelector('#copy-message').addEventListener('click', async () => {
    if (!validate()) return;
    try {
      await navigator.clipboard.writeText(body());
      status.textContent = 'Message copied. Paste it into an email to lamnv260398@gmail.com.';
    } catch {
      message.focus();
      message.select();
      status.textContent = 'Automatic copy is unavailable. Your message is selected; copy it and email lamnv260398@gmail.com.';
    }
  });
}
