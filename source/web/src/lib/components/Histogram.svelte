<!--
@component
Histogram used to display a traced beamline Element.
-->

<script lang="ts">
    import { onMount } from "svelte";

    type Props = {
        dataX: number[];
        dataY: number[];
        xLabel: string;
        yLabel: string;
        title: string;
    };

    let { dataX, dataY, xLabel, yLabel, title } = $props<Props>();
    let plotElement: HTMLDivElement;

    onMount(() => {
        let disposed = false;
        let plotly: typeof import("plotly.js-dist-min").default | undefined;
        let hasRendered = false;

        const render = async () => {
            if (!plotly) {
                const module = await import("plotly.js-dist-min");
                if (disposed) return;
                plotly = module.default;
            }
            if (disposed || dataX.length !== dataY.length || dataX.length === 0) return;

            const binCount = Math.min(200, Math.max(1, Math.floor(dataX.length / 20)));
            const minX = Math.min(...dataX);
            const maxX = Math.max(...dataX);
            const minY = Math.min(...dataY);
            const maxY = Math.max(...dataY);
            const binSizeX = (maxX - minX) / binCount || 1;
            const binSizeY = (maxY - minY) / binCount || 1;
            const countsX = histogramCounts(dataX, minX, maxX, binCount);
            const countsY = histogramCounts(dataY, minY, maxY, binCount);
            const maxXCount = Math.max(...countsX);
            const maxYCount = Math.max(...countsY);
            const meanX = dataX.reduce((sum, value) => sum + value, 0) / dataX.length;
            const meanY = dataY.reduce((sum, value) => sum + value, 0) / dataY.length;
            const stdX = standardDeviation(dataX, meanX);
            const stdY = standardDeviation(dataY, meanY);

            const traces = [
                {
                    type: "histogram2d" as const,
                    x: dataX,
                    y: dataY,
                    nbinsx: binCount,
                    nbinsy: binCount,
                    colorscale: "Viridis",
                    colorbar: {
                        title: { text: "Count" },
                        x: 0.035,
                        xanchor: "left" as const,
                        y: 0.5,
                        len: 1
                    },
                    xaxis: "x2",
                    yaxis: "y2"
                },
                {
                    type: "histogram" as const,
                    y: dataY,
                    autobinx: false,
                    ybins: { start: minY, end: maxY, size: binSizeY },
                    marker: { color: "cornflowerblue" },
                    xaxis: "x",
                    yaxis: "y"
                },
                {
                    type: "histogram" as const,
                    x: dataX,
                    autobiny: false,
                    xbins: { start: minX, end: maxX, size: binSizeX },
                    marker: { color: "cornflowerblue" },
                    xaxis: "x3",
                    yaxis: "y3"
                }
            ];

            const shapes = [
                { type: "line", xref: "x", yref: "y", x0: 0, x1: maxYCount, y0: meanY, y1: meanY, line: { color: "green", width: 2 } },
                { type: "line", xref: "x3", yref: "y3", x0: meanX, x1: meanX, y0: 0, y1: maxXCount, line: { color: "green", width: 2 } },
                { type: "line", xref: "x", yref: "y", x0: 0, x1: maxYCount, y0: meanY - stdY * 2.355 / 2, y1: meanY - stdY * 2.355 / 2, line: { color: "orange", width: 2 } },
                { type: "line", xref: "x", yref: "y", x0: 0, x1: maxYCount, y0: meanY + stdY * 2.355 / 2, y1: meanY + stdY * 2.355 / 2, line: { color: "orange", width: 2 } },
                { type: "line", xref: "x3", yref: "y3", x0: meanX - stdX * 2.355 / 2, x1: meanX - stdX * 2.355 / 2, y0: 0, y1: maxXCount, line: { color: "orange", width: 2 } },
                { type: "line", xref: "x3", yref: "y3", x0: meanX + stdX * 2.355 / 2, x1: meanX + stdX * 2.355 / 2, y0: 0, y1: maxXCount, line: { color: "orange", width: 2 } }
            ];

            // Graph Layout
            const layout = {
                autosize: true,
                height: 800,
                title: { text: title },
                margin: { l: 62, r: 28, t: 48, b: 52 },
                showlegend: false,
                bargap: 0.05,
                dragmode: "pan" as const,
                xaxis: { domain: [0.87, 1], anchor: "y", title: { text: "Count" }, showgrid: false, zeroline: false },
                yaxis: { domain: [0.15, 1], anchor: "x", matches: "y2", title: { text: yLabel }, ticks: "outside", ticklen: 6 },
                xaxis2: { domain: [0.15, 0.84], anchor: "y2", showticklabels: false, ticks: "outside", ticklen: 6 },
                yaxis2: { domain: [0.15, 1], anchor: "x2", showticklabels: false, ticks: "outside", ticklen: 6 },
                xaxis3: { domain: [0.15, 0.84], anchor: "y3", matches: "x2", title: { text: xLabel } },
                yaxis3: { domain: [0, 0.13], anchor: "x3", showgrid: false },
                shapes
            };

            // Graph Controlls
            const config = { responsive: true, scrollZoom: true, doubleClick: "reset" as const, displaylogo: false };
            if (hasRendered) await plotly.react(plotElement, traces, layout, config);
            else {
                await plotly.newPlot(plotElement, traces, layout, config);
                hasRendered = true;
            }
        };

        void render();
        return () => {
            disposed = true;
            if (plotly) plotly.purge(plotElement);
        };
    });

    function histogramCounts(values: number[], min: number, max: number, bins: number) {
        const counts = Array.from({ length: bins }, () => 0);
        const width = (max - min) / bins || 1;
        for (const value of values) counts[Math.min(bins - 1, Math.floor((value - min) / width))] += 1;
        return counts;
    }

    function standardDeviation(values: number[], mean: number) {
        return Math.sqrt(values.reduce((sum, value) => sum + (value - mean) ** 2, 0) / values.length);
    }
</script>

<div class="histogram-plot" bind:this={plotElement} aria-label="Two-dimensional histogram with marginal histograms"></div>

<style>
    .histogram-plot {
        width: 100%;
        height: 100%;
        min-height: 360px;
    }
</style>
