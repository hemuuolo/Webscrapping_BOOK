import React, { useState } from "react";
import "./index.css";
import victory from '@/assets/victory.svg';

const Auth = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleLogin = () => {
    // Example validation logic
    if (!email || !password) {
      setErrorMessage("Please fill in all fields.");
      setSuccessMessage("");
    } else {
      setErrorMessage("");
      setSuccessMessage("Login successful!");
    }
  };

  return (
    <div>
    <div className="flex items-center justify-center flex-col">
        <div className="flex items-center justify-center">
          <h1 className="text-5xl font-bold md:text-6xl">Welcome</h1>
          <img src={victory} alt="Victory Emoji" className="h-[100px]" />
        </div>
        
      </div>
      
    <div className="login-container">
      <h2 className="login-title">Login</h2>
      <form
        className="login-form"
        onSubmit={(e) => {
          e.preventDefault();
          handleLogin();
        }}
      >
        <input
          type="text"
          placeholder="Email"
          className="login-input"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="login-input"
          name="pass"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="button"
          className="btn btn-primary btn-lg custom-login-btn"
          onClick={handleLogin}
        >
          Login
        </button>
        <p>
          <b>
            <span>
              Don't have an account?{" "}
              <a href="/signup" className="signup-link">
                Signup
              </a>
            </span>
          </b>
        </p>
        <div className="login-with-google">
          <button
            type="button"
            className="btn btn-primary btn-lg btn-google"
          >
            Login with <b>Google</b>
          </button>
        </div>
      </form>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}
    </div>
    </div>
  );
};

export default Auth;
