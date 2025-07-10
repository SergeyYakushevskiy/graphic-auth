package dstu.csae.auth.graphic.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class WebController {

    @GetMapping("/login")
    public String redirectLogin() {
        return "redirect:/login.html";
    }

    @GetMapping("/register")
    public String redirectRegister() {
        return "redirect:/register.html";
    }

    @GetMapping("/two-factor")
    public String redirectTwoFactor(){
        return "redirect:/two-factor.html";
    }

    @GetMapping("/")
    public String redirectToIndex() {
        return "redirect:/index.html";
    }
}