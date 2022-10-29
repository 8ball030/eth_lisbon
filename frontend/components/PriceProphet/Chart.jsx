/* eslint-disable react/prop-types */
import React, { Component } from 'react';
import * as am5 from '@amcharts/amcharts5';
import * as am5xy from '@amcharts/amcharts5/xy';
import am5themesAnimated from '@amcharts/amcharts5/themes/Animated';

class Chart extends Component {
  componentDidMount() {
    const { ftxData } = this.props;
    const data = (ftxData || []).map((e) => ({ ...e, newTime: new Date(e.time).getTime() }));
    const root = am5.Root.new('chartdiv');
    root.setThemes([am5themesAnimated.new(root)]);

    // Create chart
    const chart = root.container.children.push(am5xy.XYChart.new(root, {
      panX: false,
      panY: false,
      wheelX: 'panX',
      wheelY: 'zoomX',
    }));

    // Add cursor
    const cursor = chart.set('cursor', am5xy.XYCursor.new(root, {
      behavior: 'zoomX',
    }));
    cursor.lineY.set('visible', false);

    // Create axes
    // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
    const xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
      groupData: true,
      maxDeviation: 0.5,
      baseInterval: { timeUnit: 'minute', count: 1 },
      renderer: am5xy.AxisRendererX.new(root, {
        minGridDistance: 50, pan: 'zoom',
      }),
    }));

    const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
      renderer: am5xy.AxisRendererY.new(root, {}),
    }));

    // Add series
    // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
    const series = chart.series.push(am5xy.LineSeries.new(root, {
      name: 'Series',
      xAxis,
      yAxis,
      valueYField: 'close',
      valueXField: 'newTime',
      tooltip: am5.Tooltip.new(root, {
        labelText: '{close}',
      }),
    }));

    // Add scrollbar
    // https://www.amcharts.com/docs/v5/charts/xy-chart/scrollbars/
    chart.set('scrollbarX', am5.Scrollbar.new(root, {
      orientation: 'horizontal',
    }));

    series.data.setAll(data);

    // Make stuff animate on load
    // https://www.amcharts.com/docs/v5/concepts/animations/
    series.appear(1000);
    chart.appear(1000, 100);

    // console.log(data);
    // ----------------
    // function addRanges() {
    //   const rangeDataItem = xAxis.makeDataItem({
    //     category: new Date(1667007240000).getTime(),
    //     endCategory: new Date(1667009640000).getTime(),
    //   });

    //   xAxis.createAxisRange(rangeDataItem);

    //   rangeDataItem.get('grid').setAll({
    //     stroke: am5.color(0x00ff33),
    //     strokeOpacity: 0.5,
    //     strokeDasharray: [3],
    //   });

    //   rangeDataItem.get('axisFill').setAll({
    //     fill: am5.color(0x00ff33),
    //     fillOpacity: 0.1,
    //     visible: true,
    //   });

    //   rangeDataItem.get('label').setAll({
    //     inside: true,
    //     text: 'Fines for speeding increased',
    //     rotation: 90,
    //     centerX: am5.p100,
    //     centerY: am5.p100,
    //     location: 0,
    //     paddingBottom: 10,
    //     paddingRight: 15,
    //   });
    // }

    // addRanges();
  }

  componentWillUnmount() {
    if (this.root) {
      this.root.dispose();
    }
  }

  render() {
    return <div id="chartdiv" style={{ width: '100%', height: '500px' }} />;
  }
}

export default Chart;
