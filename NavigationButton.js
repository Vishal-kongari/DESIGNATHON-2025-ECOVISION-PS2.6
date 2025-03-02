import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";

function NavigationButton() {
    const navigate = useNavigate();

    return (
        <Button className="ms-3" variant="outline-light" onClick={() => navigate("/dashboard")}>
            Go to Dashboard
        </Button>
    );
}

export default NavigationButton;
