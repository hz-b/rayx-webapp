<!--
@component
Graph used to display a traced reflectivity curve.
-->

<script lang="ts">
    import { ChartColumn } from "@lucide/svelte";
    import { onMount } from "svelte";

    /*
    const demoEnergy = Array.from({ length: 141 }, (_, index) => 30 + index * 0.5);
    const demoReflectivity = demoEnergy.map((energy) => {
        const envelope = 0.08 + 0.82 * Math.exp(-(((energy - 58) / 17) ** 2));
        const oscillation = 0.045 * Math.sin(energy * 0.72) + 0.02 * Math.sin(energy * 2.3);
        return Math.max(0, Math.min(1, envelope + oscillation));
    });
    */

    type Props = { dataX?: number[]; dataY?: number[]; material?: string; density?: number; angle?: number };
    type PlotlyModule = typeof import("plotly.js-dist-min").default;

    let { dataX, dataY, material, density, angle} = $props<Props>();
    let plotElement: HTMLDivElement;
    let plotly = $state<PlotlyModule | undefined>(undefined);
    let hasRendered = false;

    onMount(() => {
        let disposed = false;
        void import("plotly.js-dist-min").then((module) => {
            if (!disposed) plotly = module.default;
        });
        return () => {
            disposed = true;
            if (plotly) plotly.purge(plotElement);
        };
    });

    $effect(() => {
        const graph = plotly;
        const x = dataX;
        const y = dataY;
        const selectedMaterial = material;
        const selectedDensity = density;
        const selectedAngle = angle;
        if (!graph || !plotElement || x.length !== y.length) return;

        // Construct Plot
        const trace = [{
            type: "scatter" as const,
            mode: "lines" as const,
            name: "Reflectivity",
            x,
            y,
            line: { color: "#1769aa", width: 2 },
            hovertemplate: "Photon Energy: %{x:.2f} eV<br>Reflectivity: %{y:.5f}<extra></extra>"
        }];

        // Graph Layout
        const layout = {
            autosize: true,
            height: 700,
            margin: { l: 70, r: 24, t: 78, b: 64 },
            title: {
                text: `Reflectivity — ${selectedMaterial} · Density: ${selectedDensity === -1 ? "default" : `${selectedDensity} g/cm³`} · Angle: ${selectedAngle}°`,
                x: 0.02,
                xanchor: "left" as const
            },
            showlegend: false,
            dragmode: "pan" as const,
            xaxis: { title: { text: "Photon Energy (eV)" }, showgrid: true, gridcolor: "#e5e7eb", zeroline: false },
            yaxis: { title: { text: "Reflectivity" }, rangemode: "tozero" as const, showgrid: true, gridcolor: "#e5e7eb", zeroline: true }
        };

        // Graph Controls
        const config = { responsive: true, scrollZoom: true, doubleClick: "reset" as const, displaylogo: false };

        // Init Plot
        if (hasRendered) void graph.react(plotElement, trace, layout, config);
        else {
            void graph.newPlot(plotElement, trace, layout, config);
            hasRendered = true;
        }
    });
</script>

{#if dataX != null}
    <div class="reflectivity-plot" bind:this={plotElement} aria-label="Reflectivity by photon energy"></div>
{:else}
    <div class="Placeholder" >
        <ChartColumn size={64} strokeWidth={1}/>
        <h2>Nothing yet...</h2>
    </div>
    {/if}

<style>
    .reflectivity-plot {
        width: 100%;
        height: 100%;
        min-height: 360px;
    }

    .Placeholder {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    .Placeholder h2 {
        color: var(--color-text-on-white);
        font-weight: unset;
    }
</style>
