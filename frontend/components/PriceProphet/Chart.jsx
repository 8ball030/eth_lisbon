/* eslint-disable react/prop-types */
import React, { Component } from 'react';
import * as am5 from '@amcharts/amcharts5';
import * as am5xy from '@amcharts/amcharts5/xy';
import am5themesAnimated from '@amcharts/amcharts5/themes/Animated';
import { COLOR } from 'util/theme';

const getTimeValue = (e) => new Date(e.time).getTime();

class Chart extends Component {
  componentDidMount() {
    const { ftxData } = this.props;
    const data = (ftxData || []).map((e) => ({
      ...e,
      newTime: getTimeValue(e),
    }));
    const root = am5.Root.new('chartdiv');
    root.setThemes([am5themesAnimated.new(root)]);

    // Create chart
    const chart = root.container.children.push(
      am5xy.XYChart.new(root, {
        panX: false,
        panY: false,
        wheelX: 'panX',
        wheelY: 'zoomX',
      }),
    );

    // Add cursor
    const cursor = chart.set(
      'cursor',
      am5xy.XYCursor.new(root, {
        behavior: 'zoomX',
      }),
    );
    cursor.lineY.set('visible', false);

    // Create axes
    // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
    const xAxis = chart.xAxes.push(
      am5xy.DateAxis.new(root, {
        groupData: true,
        maxDeviation: 0.5,
        baseInterval: { timeUnit: 'minute', count: 1 },
        renderer: am5xy.AxisRendererX.new(root, {
          minGridDistance: 50,
          pan: 'zoom',
        }),
      }),
    );

    const yAxis = chart.yAxes.push(
      am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererY.new(root, {}),
      }),
    );

    // Add series
    // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
    const series = chart.series.push(
      am5xy.LineSeries.new(root, {
        name: 'Series',
        xAxis,
        yAxis,
        valueYField: 'close',
        valueXField: 'newTime',
        tooltip: am5.Tooltip.new(root, {
          labelText: '{valueY}',
          // background: {
          //   fill: COLOR.PRIMARY,
          // },
        }),
        stroke: COLOR.PRIMARY,
      }),
    );

    // Add scrollbar
    // https://www.amcharts.com/docs/v5/charts/xy-chart/scrollbars/
    chart.set(
      'scrollbarX',
      am5.Scrollbar.new(root, {
        orientation: 'horizontal',
      }),
    );

    series.data.setAll(data);

    // Make stuff animate on load
    // https://www.amcharts.com/docs/v5/concepts/animations/
    series.appear(1000);
    chart.appear(1000, 100);
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
