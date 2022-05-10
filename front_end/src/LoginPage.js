import React, { Component, useState } from 'react';
import { Button, Divider, Form, Grid, Header, Segment, Message } from 'semantic-ui-react';
import axios from "axios";
import { useNavigate } from "react-router-dom";

const api = axios.create({
    baseURL: 'https://rumzon-db.herokuapp.com/rumzon/users/'
})


function LoginPage(){

    localStorage.removeItem("userID");
    const navigate = useNavigate();
    const [user, setUser] = useState('');
    const [password, setPassword] = useState('');
    const [wrongLogin, setWrongLogin] = useState(false);
    const [enterCredentials, setEnterCredentials] = useState(false);
    //handleChange = (e, { name, value }) => this.setState({ [name]: value })

    function login(){
        navigate('/');
    }

    function checkLogin(){
        api.post('/login', { "user": user, "password": password }).then(res => {
            setEnterCredentials(false);
            setWrongLogin(false);
            localStorage.setItem("userID", res.data["User ID"]);
            localStorage.setItem("username", res.data["Username"]);
            localStorage.setItem("isAdmin", res.data["IsAdmin"]);
            login();
        }).catch(error => {
            if (error.response.status == 400) {
                console.log("Incomplete form probably");
                setWrongLogin(false);
                setEnterCredentials(true);
            }
            if (error.response.status == 404) {
                console.log("User or password incorrect");
                setEnterCredentials(false);
                setWrongLogin(true);
            }
        })
    }
            
    return<> 
        <Segment inverted>
            <Header
                as='h1'
                content='RUMZON'
                textAlign='center'
                style={{
                    fontSize: '3.5em',
                    fontWeight: 'bold',
                }}> RUMZON </Header>
            <Segment placeholder invert>
                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                icon='user'
                                iconPosition='left'
                                label='Username or Email'
                                placeholder='Username or Email'
                                value={user}
                                onChange={input => setUser(input.target.value)}
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'    
                                label='Password'
                                type='password'
                                value={password}
                                onChange={input => setPassword(input.target.value)}
                            />
                            <Message
                                hidden={!wrongLogin}
                                color={'red'}
                                header='User or password incorrect.'
                            />
                            <Message
                                hidden={!enterCredentials}
                                color={'red'}
                                header='Please enter your username/email and password.'
                            />
                            <Button content='Log in' primary onClick={checkLogin} />
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle'>
                        <Button content='Sign up' icon='signup' size='small'/>
                    </Grid.Column>
                </Grid>

                <Divider vertical>Or</Divider>
            </Segment>
        </Segment>
    </>
}

export default LoginPage;
