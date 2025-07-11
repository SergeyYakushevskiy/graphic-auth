package dstu.csae.auth.graphic.dto;

import lombok.Data;

import java.time.LocalDate;

@Data
public class RegisterRequest {
    private String login;
    private String password;
    private String mail;
    private String firstName;
    private String lastName;
    private LocalDate birthDate;
}
