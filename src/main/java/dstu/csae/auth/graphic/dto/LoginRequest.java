package dstu.csae.auth.graphic.dto;


import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class LoginRequest {

    public String identifier;
    public String password;

}
