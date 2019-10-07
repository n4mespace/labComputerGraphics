'use strict';

class PlotFormula {
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

const plot = new PlotFormula({ a: 1, b: 1 });
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
            highlightcolor:"#42f462",
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

window.onload = () => {
    const divRow = document.getElementsByClassName('row')[0];

    Plotly.react('plot', data(coords, sadlePoint), layout);
    
    divRow.style.visibility = 'visible';
    const aParam = document.getElementById('inputA');
    const bParam = document.getElementById('inputB');

    const changePlot = () => {
        const a = +aParam.value || (alert('0 is not allowed'), 1);
        const b = +bParam.value || (alert('0 is not allowed'), 1);
        const newPlot = new PlotFormula({a, b});
        const newCoords = newPlot.generateCoordsTable(100);
        const newSadlePoint = newPlot.sadlePoint;

        Plotly.react('plot', data(newCoords, newSadlePoint), layout);
    };
    aParam.onchange = changePlot;
    bParam.onchange = changePlot; 
}