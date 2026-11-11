<script>
  let { text, icon: Icon, link } = $props();
</script>

<a class="link-button" href={link} target="_blank">
  <Icon size={18} aria-hidden="true" />
  <span>{text}</span>
</a>

<style>
  .link-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.65rem 1rem;
    background: none;
    color: white;
    font: inherit;
    text-decoration: none;
    transition: background 150ms;
  }

  .link-button:hover {
    background: var(--color-label-backdrop);
  }

  .link-button:focus-visible {
    outline: 2px solid #2563eb;
    outline-offset: 3px;
  }
</style>
