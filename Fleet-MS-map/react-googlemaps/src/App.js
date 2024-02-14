import React from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import MainMap from './pages/GMap';

export default function App () {
    return (
      <Router>
          <Switch>
            <Route component={MainMap} path="/" exact/>
          </Switch>
    </Router>
    );
  }

