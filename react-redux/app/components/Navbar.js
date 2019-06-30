import React, {Component} from 'react'
import {Link, withRouter} from 'react-router-dom'

class Navbar extends React.Component {
    
    logout(e) {
        e.preventDefault()
        localStorage.removeItem('user')
        this.props.history.push("/")
    }


    render ()  {
        
        const loginRegLink = (
            <ul>
            <li className="nav-item">
                <Link className="nav-link" to="/login">Login</Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link" to="/register">Register</Link>
            </li>
            </ul>
        )

        const userLink = (
            <ul>
            <li className="nav-item">
                <Link className="nav-link" to="/profile">Profile</Link>
            </li>
            <li className="nav-item">
                <a href="" onClick={this.logout.bind(this)}>Profile</a>
            </li>

            </ul>
        )
        
        return (
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark rounded ">
                <button className="navbar-toggler" type="button" 
                    data-target="#navbar1" data-toggle="collapse"
                    data-aria-control="navbar1" data-aria-expanded="false"
                    data-aria-label="Toggle Navigation">

                </button>
                <div className="collapse navbar-collapse justify-content-md-center" id="navbar1">
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <Link to="/" className="nav-link">Home
                            </Link>
                        </li>
                    </ul>
                    {localStorage.usertoken ? userLink : loginRegLink}
                </div>    
            </nav>
        )
    }
}

export default withRouter(Navbar)