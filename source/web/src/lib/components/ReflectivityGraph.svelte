<script lang="ts">
    import { onMount } from "svelte";

    let plotElement: HTMLDivElement;

    onMount(() => {
        let disposed = false;
        let plotly: typeof import("plotly.js-dist-min").default | undefined;

        const render = async () => {
            const module = await import("plotly.js-dist-min");
            if (disposed) return;
            plotly = module.default;

            // Use a point cloud as placeholder input, matching the old 2D
            // histogram and its X/Y marginal histograms.
            const pointCount = 6000;
            const dataX = Array.from({ length: pointCount }, () => gaussianNoise());
            const dataY = Array.from({ length: pointCount }, () => gaussianNoise());
            const binCount = 40;
            const minX = Math.min(...dataX);
            const maxX = Math.max(...dataX);
            const minY = Math.min(...dataY);
            const maxY = Math.max(...dataY);
            const maxXCount = Math.max(...histogramCounts(dataX, minX, maxX, binCount));
            const maxYCount = Math.max(...histogramCounts(dataY, minY, maxY, binCount));
            const binSizeX = (maxX - minX) / binCount;
            const binSizeY = (maxY - minY) / binCount;
            const meanX = dataX.reduce((sum, value) => sum + value, 0) / pointCount;
            const meanY = dataY.reduce((sum, value) => sum + value, 0) / pointCount;
            const stdX = Math.sqrt(dataX.reduce((sum, value) => sum + (value - meanX) ** 2, 0) / pointCount);
            const stdY = Math.sqrt(dataY.reduce((sum, value) => sum + (value - meanY) ** 2, 0) / pointCount);
            const fwhmX = stdX * 2.355;
            const fwhmY = stdY * 2.355;

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
                        xanchor: "left",
                        len: 0.85
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

            const layout = {
                autosize: true,
                height: 800,
                margin: { l: 62, r: 28, t: 24, b: 52 },
                showlegend: false,
                bargap: 0.05,
                dragmode: "pan" as const,
                xaxis: {
                    domain: [0.87, 1],
                    anchor: "y",
                    title: { text: "Count" },
                    showgrid: false,
                    zeroline: false
                },
                yaxis: {
                    domain: [0.15, 1],
                    anchor: "x",
                    matches: "y2",
                    title: { text: "Y" },
                    ticks: "outside",
                    ticklen: 6
                },
                xaxis2: {
                    domain: [0.15, 0.84],
                    anchor: "y2",
                    showticklabels: false,
                    ticks: "outside",
                    ticklen: 6
                },
                yaxis2: {
                    domain: [0.15, 1],
                    anchor: "x2",
                    showticklabels: false,
                    ticks: "outside",
                    ticklen: 6
                },
                xaxis3: {
                    domain: [0.15, 0.84],
                    anchor: "y3",
                    matches: "x2",
                    title: { text: "X" }
                },
                yaxis3: {
                    domain: [0, 0.13],
                    anchor: "x3",
                    showgrid: false
                },
                shapes: [
                    // Center of mass indicators from the legacy graph.
                    { type: "line", xref: "x", yref: "y", x0: 0, x1: maxYCount, y0: meanY, y1: meanY, line: { color: "green", width: 2 } },
                    { type: "line", xref: "x3", yref: "y3", x0: meanX, x1: meanX, y0: 0, y1: maxXCount, line: { color: "green", width: 2 } },
                    // FWHM bounds on the side and bottom distributions.
                    { type: "line", xref: "x", yref: "y", x0: 0, x1: maxYCount, y0: meanY - fwhmY / 2, y1: meanY - fwhmY / 2, line: { color: "orange", width: 2 } },
                    { type: "line", xref: "x", yref: "y", x0: 0, x1: maxYCount, y0: meanY + fwhmY / 2, y1: meanY + fwhmY / 2, line: { color: "orange", width: 2 } },
                    { type: "line", xref: "x3", yref: "y3", x0: meanX - fwhmX / 2, x1: meanX - fwhmX / 2, y0: 0, y1: maxXCount, line: { color: "orange", width: 2 } },
                    { type: "line", xref: "x3", yref: "y3", x0: meanX + fwhmX / 2, x1: meanX + fwhmX / 2, y0: 0, y1: maxXCount, line: { color: "orange", width: 2 } }
                ]
            };

            await plotly.newPlot(plotElement, traces, layout, {
                responsive: true,
                scrollZoom: true,
                doubleClick: "reset",
                displaylogo: false
            });
        };

        void render();

        return () => {
            disposed = true;
            if (plotly) plotly.purge(plotElement);
        };
    });

    function gaussianNoise() {
        const u = Math.random() || Number.EPSILON;
        const v = Math.random();
        return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    }

    function histogramCounts(values: number[], min: number, max: number, bins: number) {
        const counts = Array.from({ length: bins }, () => 0);
        const width = (max - min) / bins || 1;
        for (const value of values) {
            const index = Math.min(bins - 1, Math.floor((value - min) / width));
            counts[index] += 1;
        }
        return counts;
    }
</script>

<div class="reflectivity-plot" bind:this={plotElement} aria-label="Noise-filled 2D histogram with X and Y marginal histograms"></div>

<style>
    .reflectivity-plot {
        width: 100%;
        height: 100%;
        min-height: 360px;
    }
</style>
