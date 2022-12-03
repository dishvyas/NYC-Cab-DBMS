import React from 'react';
import _ from 'lodash';
import ReactECharts from 'echarts-for-react';
import { Message } from 'semantic-ui-react';

class PieChartData extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        var data = this.props.data;
        
       data = _.keys(data).map((key) => {
        return {name:  key, value: data[key]}});
        console.log(data);
        var option = {
            tooltip: {
              trigger: 'item'
            },
            legend: {
              top: '100%',
              left: 'center'
            },
            series: [
              {
                name: 'Access From',
                type: 'pie',
                radius: ['0%', '70%'],
                avoidLabelOverlap: false,
                label: {
                  show: false,
                  position: 'center'
                },
                emphasis: {
                  label: {
                    show: true,
                    fontSize: '40',
                    fontWeight: 'bold'
                  }
                },
                labelLine: {
                  show: false
                },
                data: data
              }
            ]
          };
          console.log(data);
        return  <div>
            <Message>
    <Message.Header>Employment Distribution</Message.Header>
    <p>
      The piechart displays the employment distribution across various sectors
    </p>
  </Message>
        <ReactECharts option={option}   />;
        </div>

    }


}

export default PieChartData;