import React, {useState} from 'react';
import {Grid, Dropdown, Button} from 'semantic-ui-react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import axios from 'axios'
import _ from 'lodash'

class Filter extends React.Component{
    constructor(props){
        super(props);
        console.log(this.props)
        


        this.state = {start_date: new Date(2019, 0, 1), end_date: new Date(2020, 11, 31), duration: 'month', count: 0};
    }

    onChangeDate = (val, e, name) => {
        console.log(val, name, e);
        // this.setState({dateTime: val}, () => {
        // this.props.updateRootParams(this.state);
        // });
    }

    onChangeParams = (key, val) =>{
        this.setState({[key]: val}, () => {
            this.props.updateRootParams(this.state);
        });
    }

    componentWillReceiveProps = (prevProps, currProps)=>{
        console.log(prevProps, currProps);

    }

    fetchCount = () => {
        axios.get(`http://127.0.0.1:5000/fetch_count`).then((res) => {
            this.setState({count: res.data.count})
        })
    }

    render(){
    var numberOfClusters = ["month", "year"].map((x) => {return {key: x, value: x, text: x}});
    return <Grid columns={4}>
    <Grid.Row>
      <Grid.Column textAlign={'center'} style = {{marginTop: '0.5rem'}}> 
      <DatePicker  selected={this.state.start_date} minDate = {new Date(2019, 0, 1)} maxDate = {new Date(2020, 11, 31)}  onChange={(val) => {
        this.setState({start_date: val}, () => {
            this.props.updateRootParams(this.state);
        });
      }} />

      </Grid.Column>
      <Grid.Column textAlign={'center'} style = {{marginTop: '0.5rem'}}> 
      <DatePicker selected={this.state.end_date} minDate = {new Date(2019, 0, 1)} maxDate = {new Date(2020, 11, 31)} onChange={(val) => {
        this.setState({end_date: val}, () => {
            this.props.updateRootParams(this.state);
        });
      }} />
      </Grid.Column>
      <Grid.Column textAlign={'center'}>
        <Dropdown placeholder='Duration' value={this.state.duration} search selection options={numberOfClusters} onChange={(e, {value})=>{
            this.onChangeParams('duration', value);
        }} />
      </Grid.Column>
      <Grid.Column textAlign={'center'}>
        <Button color={'teal'} size = {'tiny'} onClick = {this.fetchCount}>{(this.state.count === 0)?"Count":this.state.count }</Button>
      </Grid.Column>
      
    </Grid.Row>
  </Grid>
    }
}

export default Filter;