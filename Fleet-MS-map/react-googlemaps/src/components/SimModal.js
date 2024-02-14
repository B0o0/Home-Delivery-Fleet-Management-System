import  React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import { startSimulation } from '../api/Simulation';
import FormattedInputs from './IntInput';
import LinearProgress from '@mui/material/LinearProgress';
import SimStartedSnackbars from './simsnackBar';

export default function SimDialog({socket}) {
  const [open, setOpen] = useState(false);
  const [Started, setStarted] = useState(false);
  const [Speed, setSpeed] = useState('R');
  const [startedSuccess, setStartedSuccess] = useState(false);
  const [startedSuccessOpen, setStartedSuccessOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleSubmit = () => {
    setOpen(false);
    setStarted(true);
    const speed = document.getElementById("sim-speed").value
    const drivers_number = document.getElementById("formatted-numberformat-input").value
    startSimulation(speed, drivers_number).then((res)=> {
      console.log(res);
      setStarted(false);
      setStartedSuccess(true);
      setStartedSuccessOpen(true);

    })
  };

  const handleSpeedChange = (event) => {
    setSpeed(
      event.target.value,
    );
  };

  useEffect(() =>{

    socket.emit("get_sim_status", (status)=>{
      setStartedSuccess(status);
    })


  }, [socket])


  return (
    <React.Fragment>
      {Started ? 
      <Box sx={{ width: '100%'  }}>
      <LinearProgress />
      </Box> :
      <>
      {
        startedSuccess ? (""):
        (
          <Button onClick={handleClickOpen}>
           start simulation
          </Button>
        )
      }
      </>
      }
      {
      startedSuccessOpen ?
      <SimStartedSnackbars
      setOpen={setStartedSuccessOpen}
      open={startedSuccessOpen}
      message={"Started simulation successfully!"}
      />
      :
      <></>
      }
      <Dialog
        fullWidth={true}
        maxWidth={'sm'}
        open={open}
        onClose={handleClose}
      >
        <DialogTitle>Simulation Options</DialogTitle>
        <DialogContent>
          <Box
            noValidate
            component="form"
            sx={{
              display: 'flex',
              flexDirection: 'column',
              m: 'auto',
              width: 'fit-content',
            }}
          >
            <FormControl sx={{ mt: 2, minWidth: 120 }}>
              <InputLabel htmlFor="max-width">Speed</InputLabel>
              <Select
                autoFocus
                value={Speed}
                onChange={handleSpeedChange}
                label="speed"
                inputProps={{
                  name: 'sim-speed',
                  id: 'sim-speed',
                }}
              >
                <MenuItem value="F">Fast</MenuItem>
                <MenuItem value="R">Real</MenuItem>
                <MenuItem value="S">Slow</MenuItem>

              </Select>
              <FormattedInputs/>

            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleSubmit}>Submit</Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}