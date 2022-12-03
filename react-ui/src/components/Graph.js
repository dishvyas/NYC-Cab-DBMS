import React from 'react'
import ReactECharts from 'echarts-for-react';
import _ from 'lodash'
import {Message} from 'semantic-ui-react'

class Graph extends React.Component{
    constructor(props){
        super(props);
        this.state = {};
    }


     onChartClick = (params) => {
        console.log('Chart clicked', params, this.state.xAxisData[params.dataIndex]);
        var parameters = this.state.xAxisData[params.dataIndex].toString().split("-");
        var filters = {};
        
        if(parameters.length == 1){
            filters['year'] = parameters[0];
            filters['duration'] = 'year'
        }else{
            filters['month'] = parameters[0];
            filters['year'] = parameters[1];
            filters['duration'] = 'month'
        }
        console.log(filters);
        this.props.fetch_employment_details(filters);
        
      };

    render(){
        
        this.state.data = this.props.data;
        if(!_.isEmpty(this.state.data)){
        var xAxisData = []
        if(this.state.data.length > 0 && "MONTH_NAME" in this.state.data[0])
           this.state.xAxisData = this.props.data.map((x) => `${x.MONTH_NAME}-${x.YEAR_NAME}`);
        else
            this.state.xAxisData = this.props.data.map((x) => x.YEAR_NAME);

        this.state.tripCount = this.props.data.map((x) => x.NUMBER_OF_TRIPS);
        this.state.employeeCount = this.props.data.map((x) => x.EMPLOYMENT_COUNT);


        var emphasisStyle = {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0,0,0,0.3)'
            }
          };
          var options = {
            legend: {
              data: ['Trips', 'Employment'],
              left: '10%'
            },
            brush: {
              xAxisIndex: 0
            },
            toolbox: {
              feature: {
                magicType: {
                  type: ['stack']
                },
                dataView: {}
              }
            },
            tooltip: {},
            xAxis: {
              data: this.state.xAxisData,
              name: 'Duration',
              axisLine: { onZero: true },
              splitLine: { show: false },
              splitArea: { show: false }
            },
            yAxis: {},
            grid: {
              bottom: 100
            },
            series: [
              {
                name: 'Trips',
                type: 'bar',
                stack: 'one',
                emphasis: emphasisStyle,
                data: this.state.tripCount
              },
             ,
              {
                name: 'Employment',
                type: 'bar',
                stack: 'two',
                emphasis: emphasisStyle,
                data: this.state.employeeCount
              },
              
            ]
          };

  

  const onEvents = {
    click: this.onChartClick,
  };
          return <div>
            <Message>
    <Message.Header>Trip VS Employment</Message.Header>
    <p>
        The graph shows how trip and employment are correlated across the time
    </p>
  </Message>
          <ReactECharts option={options}       onEvents={onEvents}
          />
          </div>
        }return null;
    }


}

export default Graph;