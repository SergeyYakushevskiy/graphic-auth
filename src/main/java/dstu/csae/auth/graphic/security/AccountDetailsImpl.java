package dstu.csae.auth.graphic.security;

import dstu.csae.auth.graphic.model.Account;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;
import java.util.UUID;

@Data
@AllArgsConstructor
public class AccountDetailsImpl implements UserDetails {

    private String identifier;
    private UUID id;
    private String login;
    private String password;
    private String mail;

    public static AccountDetailsImpl build(Account account, String identifier, String passwordHash){
        return new AccountDetailsImpl(
                identifier,
                account.getId(),
                account.getLogin(),
                passwordHash,
                account.getEmail()
        );
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of();
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return login;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
