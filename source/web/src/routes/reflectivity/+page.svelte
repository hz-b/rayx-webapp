<script lang="ts">
    import ContentWindow from "#lib/components/ContentWindow.svelte";
    import Header from "#lib/components/Header.svelte";
    import ReflectivityTraceSettings from "#lib/components/ReflectivityTraceSettings.svelte";
</script>

<Header/>
<main>
    <ContentWindow title="Settings" width={30} expandable>
        <ReflectivityTraceSettings endpoint="/api/trace" />
    </ContentWindow>
    <ContentWindow title="Graph Viewer" width={70}>
        <p>Graph will be displayed here.</p>
    </ContentWindow>
</main>

<style>
    main{
        margin: 2rem;
        display: flex;
        height: 80vh;
    }
</style>
