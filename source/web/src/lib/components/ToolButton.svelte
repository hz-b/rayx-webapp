<script lang="ts">
    let { text, isSelected = false, link} = $props();
</script>

<a href={link} class:selected={isSelected}>{text}</a>

<style>
    a {
        border-radius: 10px;
        padding: 0 0.2rem;
    }

    a:hover {
        text-decoration: underline;
    }

    a.selected {
        background-color: white;
        color: black;
    }

    a.selected:hover {
        text-decoration: none;
    }
</style>
