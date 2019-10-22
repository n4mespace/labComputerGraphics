'use strict';



class PlotFormula3D {
    constructor({a, b}) {
        this.a = a;
        this.b = b;
    }

    formulaForZ(x, y) { 
        return ((x - this.a)**2 / this.a) - ((y - this.b)**2 / this.b);
    }

    generateCoordsTable(n) {
        const coordsTable = [];
        for (let x = -n; x < n; x++) {
            const row = [];
            for (let y = -n; y < n; y++) {
                row.push(this.formulaForZ(x, y));
            }
            coordsTable.push(row);
        }
        return coordsTable;
    };

    get sadlePoint() {
        const x = this.b + 100;
        const y = this.a + 100;
        const z = this.formulaForZ(this.a, this.b);  // === 0
        return { x, y, z };
    };
}

const plot = new PlotFormula3D({ a: 1, b: 1 });
const coords = plot.generateCoordsTable(100);
const sadlePoint = plot.sadlePoint;

const data = (coords, sadlePoint) => ([{
    z: coords,
    opacity: 0.8,
    type: 'surface',
    hoverinfo: 'x+y+z',
    contours: {
        z: {
            show:true,
            usecolormap: true,
            highlightcolor:'#42f462',
            project:{z: true},
        },
    },
}, {
    x: [sadlePoint.x],
    y: [sadlePoint.y],
    z: [sadlePoint.z],
    mode: 'markers',
    type: 'scatter3d',
    marker: {
      color: 'rgb(23, 190, 207)',
      size: 15,
    },
    hoverinfo: 'x+y+z',
}]);                                                                                                                                                                                                                              

const layout = {
    title: 'Chart for formula',
    hovermode: 'closest',
    scene: {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        camera: {
            eye: {
                x: 1.87,
                y: 0.61,
                z: 0.98,
            }
        }
    },
    autosize: false,
    width: 600,
    height: 600,
    margin: {
        l: 0, b: 0,
        t: 0, r: 0,
    },
    
};


class PlotFormula2D {
    constructor({ a, b, z, n } ) {
        this.a = a;
        this.b = b;
        this.z = z;

        const X = [];
        for (let x = -n; x <= n; x++) {
            X.push(x);
        }
        this.X = X;
    }

    formulaY(x) {
        return Math.sqrt(
            this.b * ((x - this.a)**2 / this.a - this.z)
            ) + this.b;                                                                                                                                                                                                                                                                                                                                                  ;
    }

    generateXY() {        
        const Y = this.X.map(x => this.formulaY(x));
        return { X: this.X, Y };
    }
}

const plot2d = new PlotFormula2D({ a: 1, b: 1, z: 0, n: 100 });    
const { X: plot2dX, Y: plot2dY } = plot2d.generateXY();

const data2dplot = (plot2dX, plot2dY) => [{
    x: plot2dX,
    y: plot2dY,
    mode: 'line',
    name: '',
    line: {
        color: 'blue',
        width: 3,
        shape: 'spline',
    }
}, {
    x: plot2dX,
    y: plot2dY.map(y => -y),
    mode: 'line',
    name: '',
    line: {
        shape: 'spline',
        color: 'blue',
        width: 3,
    }
}]

const layout2dplot = {
    showlegend: false,
}

const sliceCenter = (arr, right=10, left=11) => {
    const center = arr.length / 2;
    return arr.slice(center - right, center + left);
};

const dataHistogram = (plot2dX, plot2dY) => [{
    type: 'bar',
    x: sliceCenter(plot2dX, 20, 21),
    y: sliceCenter(plot2dY, 20, 21),
    marker: {
      color: 'blue'
    },
}, {
    type: 'bar',
    x: sliceCenter(plot2dX, 20, 21),
    y: sliceCenter(plot2dY.map(y => -y), 20, 21),
    marker: {
      color: 'red'
    },
}]

const dataPieChart = (plot2dX, plot2dY) => [{
    values: sliceCenter(plot2dX),
    labels: sliceCenter(plot2dY),
    type: 'pie'
}]

const pieChartlayout = {
    showlegend: false,
    height: 500,
    width: 600
  };

const makeTable = (X, Y) => [{
    type: 'table',
    header: {
        values: [["<B>X</B>"], ["<B>Y</B>"]],
        align: ["center"],
        fill: {
            color: '#119DFF',
        },
        font: {
            family: "Arial", 
            size: 14, 
            color: "white",
        },
    },
    cells: {
        values: [ 
            sliceCenter(X), 
            sliceCenter(Y), 
        ],
        align: 'center',
        line: {
            color: [ 'black' ],
            width: 1,
        },
        font: {
            family: 'Arial', 
            size: 11, 
            color: [ 'black' ],
        },
    }
}];


window.onload = () => {
    const divRows = [...document.getElementsByClassName('row')];

    Plotly.react('plot3D', data(coords, sadlePoint), layout);
    Plotly.react('2Dchart', data2dplot(plot2dX, plot2dY), layout2dplot);
    Plotly.react('hist', dataHistogram(plot2dX, plot2dY), layout2dplot);
    Plotly.react('info-table', makeTable(plot2dX, plot2dY));
    Plotly.react('pie', dataPieChart(plot2dX, plot2dY), pieChartlayout);

    divRows.forEach(div => div.style.visibility = 'visible');

    const aParam = document.getElementById('inputA');
    const bParam = document.getElementById('inputB');
    const aValue = () => +aParam.value || 1;
    const bValue = () => +bParam.value || 1;

    const changePlot = () => {
        const a = aValue();
        const b = bValue();
        const newPlot = new PlotFormula3D({ a, b });
        const newCoords = newPlot.generateCoordsTable(100);
        const newSadlePoint = newPlot.sadlePoint;

        Plotly.react('plot', data(newCoords, newSadlePoint), layout);
    };
    aParam.onchange = changePlot;
    bParam.onchange = changePlot;

    const zParam = document.getElementById('inputZ');
    const zValue = () => +zParam.value;

    const change2dPlots = () => {
        const a = aValue();
        const b = bValue();
        const z = zValue();

        const newPlot2d = new PlotFormula2D({ a, b, z, n: 500 });
        const { X: newX, Y: newY} = newPlot2d.generateXY();

        Plotly.react('2Dchart', data2dplot(newX, newY), layout2dplot);
        Plotly.react('hist', dataHistogram(newX, newY), layout2dplot);
        Plotly.react('pie', dataPieChart(newX, newY), pieChartlayout);
        Plotly.react('info-table', makeTable(newX, newY), layout2dplot);
    };
    zParam.onchange = change2dPlots;
}