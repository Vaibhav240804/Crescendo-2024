import React, { useEffect, useState } from 'react';
// import data from '../data/dummyData.json';
import Center from '../animated-components/Center'
import Star from '../components/dashboard/Star';
import Sva from '../components/dashboard/Sva';
import Keyword from '../components/dashboard/Keyword';
import Sentiment from '../components/dashboard/Sentiment';
import TextField from '@mui/material/TextField';
import { Spin as Hamburger } from 'hamburger-react'
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import Api from '../api';
import { CircularProgress, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { useSelector, useDispatch } from 'react-redux';
import AddIcon from '@mui/icons-material/Add';
import { setCurrProd } from '../redux/features/userslice';
import PropTypes from 'prop-types';
import { styled } from '@mui/material/styles';
import Rating from '@mui/material/Rating';
import SentimentVeryDissatisfiedIcon from '@mui/icons-material/SentimentVeryDissatisfied';
import SentimentDissatisfiedIcon from '@mui/icons-material/SentimentDissatisfied';
import SentimentSatisfiedIcon from '@mui/icons-material/SentimentSatisfied';
import SentimentSatisfiedAltIcon from '@mui/icons-material/SentimentSatisfiedAltOutlined';
import SentimentVerySatisfiedIcon from '@mui/icons-material/SentimentVerySatisfied';

const StyledRating = styled(Rating)(({ theme }) => ({
    '& .MuiRating-iconEmpty .MuiSvgIcon-root': {
        color: theme.palette.action.disabled,
    },
}));

const customIcons = {
    1: {
        icon: <SentimentVeryDissatisfiedIcon color="error" />,
        label: 'Very Dissatisfied',
    },
    2: {
        icon: <SentimentDissatisfiedIcon color="error" />,
        label: 'Dissatisfied',
    },
    3: {
        icon: <SentimentSatisfiedIcon color="warning" />,
        label: 'Neutral',
    },
    4: {
        icon: <SentimentSatisfiedAltIcon color="success" />,
        label: 'Satisfied',
    },
    5: {
        icon: <SentimentVerySatisfiedIcon color="success" />,
        label: 'Very Satisfied',
    },
};

function IconContainer(props) {
    const { value, ...other } = props;
    return <span {...other}>{customIcons[value].icon}</span>;
  }
  
  IconContainer.propTypes = {
    value: PropTypes.number.isRequired,
  };

const Dashboard = () => {
    const dispatch = useDispatch();
    const user = JSON.parse(localStorage.getItem('user'));
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState();
    const [state, setState] = useState(false);
    const prod = useSelector((state) => state.user.currProd);

    const [url, setUrl] = useState('');
    // console.log(data);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            await Api.sendProducts({ email: user.email })
                .then((res) => {
                    console.log(res.data);
                    setData(res.data.products);
                    setLoading(false);
                })
                .catch((err) => {
                    console.log(err);
                    // setLoading(false);
                })
        }
        fetchData();
    }, []);

    const toggleDrawer = (open) => (event) => {
        if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
            return;
        }

        setState(open);
    };

    const list = (data) => (
        <Box
            sx={{ width: 300, marginTop: 8 }}
            role="presentation"
            onClick={toggleDrawer(false)}
            onKeyDown={toggleDrawer(false)}
        >
            <div className='fixed top-4 left-[230px]'>
                <IconButton>
                    <Hamburger
                        size={30}
                        color='black'
                        toggled={state}
                        toggle={setState}
                    />
                </IconButton>
            </div>
            <div className='mt-2 text-2xl font-bold w-full text-center mb-2'>
                Previous Searches
            </div>
            <Divider />
            <List>
                <ListItem disablePadding>
                    <ListItemButton onClick={() => {
                        dispatch(setCurrProd(null));
                    }}>
                        <ListItemIcon>
                            {<AddIcon />}
                        </ListItemIcon>
                        <ListItemText primary={"New Product"} />
                    </ListItemButton>
                </ListItem>
                {data?.map((text, index) => (
                    <ListItem key={text._id} disablePadding>
                        <ListItemButton onClick={() => {
                            dispatch(setCurrProd(text));
                        }}>
                            <ListItemText primary={text.name} secondary={text.date} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>
        </Box>
    );

    return (
        <>
            {loading ?
                (<Center>
                    <CircularProgress
                        sx={{
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                        }}
                    />
                </Center>)
                : (<Center>
                    <div className='w-full h-full p-4 flex flex-col items-start gap-4'>
                        <div className='fixed'>
                            <IconButton>
                                <Hamburger
                                    size={30}
                                    color='black'
                                    toggled={state}
                                    toggle={setState}
                                />
                            </IconButton>
                        </div>
                        <Drawer
                            anchor={'left'}
                            open={state}
                            onClose={toggleDrawer(false)}
                        >
                            {list(data)}
                        </Drawer>
                        <>
                            {!prod ? (<>
                                <div className='w-full flex flex-col items-center justify-center gap-4 text-center font-bold text-3xl'>
                                    <div>
                                        Dashboard
                                    </div>
                                    <div className='w-[60%] flex items-center gap-2'>
                                        <TextField
                                            label='Enter URL'
                                            variant='outlined'
                                            fullWidth
                                            value={url}
                                            onChange={(e) => setUrl(e.target.value)}
                                        />
                                        <IconButton
                                            color='primary'
                                            onClick={() => {
                                                console.log(url);
                                            }}
                                        >
                                            <SendIcon sx={{
                                                fontSize: 40,
                                                color: '#33006F'
                                            }} />
                                        </IconButton>
                                    </div>
                                </div>
                                <div className='w-full h-[31.5vh] text-center text-xl font-bold mt-16'>
                                    Please Enter an Amazon URL to get started
                                </div>
                                <button>

                                </button>
                            </>)
                                :
                                (<div className='w-full flex flex-col items-center gap-8 justify-center'>
                                    <div className='flex items-center justify-between p-2 bg-white shadow-xl rounded-xl text-center w-[90%]'>
                                        <div className='w-[20%]'>
                                            <img src={prod.image} alt="product" width="100%" className='cursor-pointer' onClick={() => {
                                                window.open(prod.url);
                                            }} />
                                        </div>
                                        <div className='w-[60%] flex flex-col items-start justify-normal gap-1 text-justify'>
                                            <span className='font-bold text-black text-center'>
                                                {prod.name}
                                            </span>
                                            <span className='font-bold text-black text-opacity-65 text-xs'>
                                                {prod.description}
                                            </span>
                                        </div>
                                        <div className='w-[15%] flex flex-col items-center justify-center gap-2 text-justify'>
                                            <span className='font-bold text-2xl tracking-wide'>
                                                {prod.price}
                                            </span>
                                            <span className='font-semibold text-sm text-black text-opacity-40'>
                                                {prod.date}
                                            </span>
                                            <span className='text-xs text-blue-600 hover:underline cursor-pointer' onClick={() => {
                                                window.open(prod.url);
                                            }}>
                                                View on Amazon
                                            </span>
                                            <span>
                                                <StyledRating
                                                    name="highlight-selected-only"
                                                    // calc the average rating of product
                                                    readOnly
                                                    value={prod.avgRating}
                                                    IconContainerComponent={IconContainer}
                                                    getLabelText={(value) => customIcons[value].label}
                                                    highlightSelectedOnly
                                                />
                                            </span>
                                        </div>
                                    </div>
                                    <div className='flex items-center justify-center gap-4'>
                                        <div className=''>
                                            <h2>Sentiment</h2>
                                            <div className='p-2 bg-white shadow-md rounded-xl'>
                                                <Sentiment data={prod} />
                                            </div>
                                        </div>
                                        <div>
                                            <h2>Star Ratings Distribution</h2>
                                            <div className='p-2 bg-white shadow-md rounded-xl'>
                                                <Star data={prod} />
                                            </div>
                                        </div>
                                    </div>
                                    <div className='flex items-center justify-center gap-4'>
                                        <div className=''>
                                            <h2>Keywords</h2>
                                            <div className='p-2 bg-white shadow-md rounded-xl'>
                                                <Keyword data={prod} />
                                            </div>

                                        </div>
                                        <div>
                                            <h2>Seasonal Variation Analysis</h2>
                                            <div className='p-2 bg-white shadow-md rounded-xl'>
                                                <Sva data={prod} />
                                            </div>
                                        </div>
                                    </div>
                                </div>)}
                        </>
                    </div>
                </Center>)}
        </>
    );
};

export default Dashboard;