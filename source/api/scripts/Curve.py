#region Imports
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scripts.HistogramData import HistogramData
import base64
# endregion


class Curve:
    """
    A curve plot (e.g. reflectivity vs photon energy).
    Uses Plotly for interactive visualization.
    """

    def __init__(self, dataX, dataY, xLabel="No label", yLabel="No label", title="No title", incoming=[], outgoing=[], incoming_efields=[], outgoing_efields=[]):

        self.curveDataX = np.array(dataX)
        self.curveDataY = np.array(dataY)

        self.incoming = np.array(incoming)
        self.outgoing = np.array(outgoing)

        self.incoming_efields = incoming_efields
        self.outgoing_efields = outgoing_efields

        self.xlabel = xLabel
        self.ylabel = yLabel
        self.title = title

        self.plot_html = self.GetPlotHTML()

    @staticmethod
    def fmt_complex(val):
        """
        Returns a string representation of a complex number.
        """
        
        if isinstance(val, complex):
            sign = "+" if val.imag >= 0 else ""
            return f"{val.real:.5f}{sign}{val.imag:.5f}j"
        try:
            return f"{float(val):.5f}"
        except (TypeError, ValueError):
            return str(val)

    def GetPlotHTML(self) -> str:
        """
        Returns interactive Plotly HTML for a curve plot. For better debugging this class also plots a table of the data points.
        """

        # Create figure
        fig = make_subplots(
            rows=3, cols=1,
            row_heights=[0.5, 0.25, 0.25],  # main vs table
            vertical_spacing=0.1,
            specs=[
                [{"type": "xy"}],      # row 1: the curve
                [{"type": "domain"}],   # row 2: the table
                [{"type": "domain"}]   # row 3: the table
            ]
        )

        # Add reflectivity curve
        fig.add_trace(
            go.Scatter(
                x=self.curveDataX,
                y=self.curveDataY,
                mode="lines",
                name="Reflectivity"
            ), row=1, col=1
        )

        # Add data table
        fig.add_trace(
            go.Table(
                header=dict(values=["Photon Energy (eV)", "Reflectivity"]),
                cells=dict(values=[self.curveDataX, self.curveDataY])
            ), row=2, col=1
        )

        # E-field table
        fig.add_trace(
            go.Table(
                header=dict(values=["eV", "In Ex", "In Ey", "In Ez", "Out Ex", "Out Ey", "Out Ez"]),
                cells=dict(values=[
                    self.curveDataX,
                    [self.fmt_complex(e.get("ex", float("nan"))) for e in self.incoming_efields],
                    [self.fmt_complex(e.get("ey", float("nan"))) for e in self.incoming_efields],
                    [self.fmt_complex(e.get("ez", float("nan"))) for e in self.incoming_efields],
                    [self.fmt_complex(e.get("ex", float("nan"))) for e in self.outgoing_efields],
                    [self.fmt_complex(e.get("ey", float("nan"))) for e in self.outgoing_efields],
                    [self.fmt_complex(e.get("ez", float("nan"))) for e in self.outgoing_efields],
                ])
            ), row=3, col=1
        )

        # Layout
        fig.update_layout(
            height=1000,
            width=1000,
            title=self.title,
            xaxis_title=self.xlabel,
            yaxis_title=self.ylabel,
            showlegend=False,
            dragmode="pan",
        )

        # Controls
        fig.update_layout(
            dragmode="pan"
        )

        # construct HTML
        plot_html = fig.to_html(
            full_html=False,
            include_plotlyjs="cdn",
            config={
                "scrollZoom": True,
                "doubleClick": "reset",
                "displaylogo": False
            }
        )

        # region Debugging
        # Build CSV content
        rows = ["eV,In Ex,In Ey,In Ez,Out Ex,Out Ey,Out Ez"]
        for i, eV in enumerate(self.curveDataX):
            ie = self.incoming_efields[i] if i < len(self.incoming_efields) else {}
            oe = self.outgoing_efields[i] if i < len(self.outgoing_efields) else {}
            rows.append(",".join([
                str(eV),
                str(ie.get("ex", "")),
                str(ie.get("ey", "")),
                str(ie.get("ez", "")),
                str(oe.get("ex", "")),
                str(oe.get("ey", "")),
                str(oe.get("ez", "")),
            ]))
        csv_content = "\n".join(rows)

        # Inject download button
        csv_bytes = csv_content.encode("utf-8")
        csv_b64 = base64.b64encode(csv_bytes).decode("utf-8")

        download_btn = f"""
        <div class="DebuggerMenu" style="background-color: tomato;">
        <h2>DEBUGGER MENU</h2>
        <a href="data:text/csv;base64,{csv_b64}" download="efields.csv"
        style="display:inline-block; margin: 10px; padding: 8px 16px; 
                cursor: pointer; background:#eee; border:1px solid #ccc; 
                text-decoration:none; color:black;">
            Download E-field CSV
        </a>
        """
        # endregion

        # TODO: Remove download button if not debugging
        return plot_html + download_btn