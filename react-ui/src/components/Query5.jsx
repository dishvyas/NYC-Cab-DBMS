import React from 'react'
import Filter from './Filter'
import Graph from './Graph'
// import axios from './axios'
import * as moment from 'moment'
import _ from 'lodash'
import axios from 'axios'
import PieChartData from './PieChartData'

class  Query5 extends React.Component{
    constructor(props){
        super(props);
        this.state = {data: []};
    }

    fetchTripToMonthMapper = (params) => {
        axios.post(`http://127.0.0.1:5000/fetch_trips_to_employment_map`, params).then((res)=>{
            this.setState({data: res.data});
        })   
    }

    fetch_employment_details = (params) => {
        axios.post(`http://127.0.0.1:5000/fetch_employment_details`, params).then((res)=>{
            var data = _.reduce(res.data, (prev, curr) => {
                if(!(curr['INDUSTRY_TITLE'] in prev))
                    prev[curr['INDUSTRY_TITLE']] = 0 
                prev[curr['INDUSTRY_TITLE']] += curr['EMPLOYEE_COUNT'];
                return prev;
            }, {});
            console.log(data)
            this.setState({pieChartData: data});
        })
    }

    componentDidMount = () => {
        this.fetchTripToMonthMapper({start_date: "01-Jan-2019", end_date: "31-Dec-2020", duration: "month"})
    }

    onChangeParams = (params) => {
        var data = _.cloneDeep(params);
        data['start_date'] = moment(data['start_date']).format('DD-MMM-YYYY');
        data['end_date'] = moment(data['end_date']).format('DD-MMM-YYYY');
        console.log(data)
        this.fetchTripToMonthMapper(data);   
    }


render(){
return <div style={{ marginLeft: '2rem', marginTop: '2rem'}}>
<Filter updateRootParams={this.onChangeParams}/>
<div style={{marginTop: '4rem'}}>
    <Graph data={this.state.data} fetch_employment_details={this.fetch_employment_details}/></div>
    {_.isEmpty(this.state.pieChartData)?null:<PieChartData data={this.state.pieChartData}/>}
</div>

return null;
}
}
export default Query5;