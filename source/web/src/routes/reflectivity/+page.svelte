<script lang="ts">
    import ContentWindow from "#lib/components/ContentWindow.svelte";
    import Header from "#lib/components/Header.svelte";
    import ReflectivityTraceSettings from "#lib/components/ReflectivityTraceSettings.svelte";
    import ReflectivityGraph from "#lib/components/ReflectivityGraph.svelte";

    let traceResult = $state<{
        dataX: number[];
        dataY: number[];
        material: string;
        density: number;
        angle: number;
    } | null>(null);
</script>

<Header/>
<main>
    <ContentWindow title="Settings" width={30} expandable>
        <ReflectivityTraceSettings
            endpoint="http://localhost:8000/api/reflectivity"
            onTrace={(result) => (traceResult = result)}
        />
    </ContentWindow>
    <ContentWindow title="Graph Viewer" width={70}>
        <ReflectivityGraph
            dataX={traceResult?.dataX}
            dataY={traceResult?.dataY}
            material={traceResult?.material}
            angle={traceResult?.angle}
            density={traceResult?.density}
        />
    </ContentWindow>
</main>

<style>
    main{
        margin: 2rem;
        display: flex;
        height: 80vh;
    }
</style>
