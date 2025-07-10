package dstu.csae.auth.graphic.service;

import dstu.csae.auth.graphic.model.Account;
import dstu.csae.auth.graphic.model.PasswordHash;
import dstu.csae.auth.graphic.repository.AccountRepository;
import dstu.csae.auth.graphic.repository.PasswordHashRepository;
import dstu.csae.auth.graphic.security.AccountDetailsImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class AccountService implements UserDetailsService {

    private AccountRepository accountRepository;
    private PasswordHashRepository passwordHashRepository;

    @Autowired
    public void setAccountRepository(AccountRepository accountRepository,
                                     PasswordHashRepository passwordHashRepository){
        this.accountRepository = accountRepository;
        this.passwordHashRepository = passwordHashRepository;
    }

    @Override
    public AccountDetailsImpl loadUserByUsername(String login)
            throws UsernameNotFoundException {
        Account account = accountRepository.findByLogin(login).orElseThrow(
                () -> new UsernameNotFoundException(
                        String.format("Пользователь с именем %s не найден", login))
        );
        PasswordHash passwordHash = passwordHashRepository.findFirstByAccount_IdOrderByCreatedAtDesc(account.getId()).orElseThrow(
                () -> new RuntimeException(String.format("Пользователь %s неверно зарегистрирован", login))
        );

        return AccountDetailsImpl.build(account, login, passwordHash.getHash());
    }

    public AccountDetailsImpl loadUserByEmail(String email)
            throws UsernameNotFoundException {
        Account account = accountRepository.findByEmail(email).orElseThrow(
                () -> new UsernameNotFoundException(
                        String.format("Пользователь с почтой %s не найден", email))
        );
        PasswordHash passwordHash = passwordHashRepository.findFirstByAccount_IdOrderByCreatedAtDesc(account.getId()).orElseThrow(
                () -> new RuntimeException(String.format("Пользователь %s неверно зарегистрирован", email))
        );
        return AccountDetailsImpl.build(account, email, passwordHash.getHash());
    }

    public AccountDetailsImpl loadByIdentifier(String identifier) {
        if (identifier.matches("^[\\w-.]+@[\\w-]+\\.[a-zA-Z]{2,}$")) {
            return loadUserByEmail(identifier);
        } else {
            return loadUserByUsername(identifier);
        }
    }

}
