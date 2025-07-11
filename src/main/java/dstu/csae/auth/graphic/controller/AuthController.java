package dstu.csae.auth.graphic.controller;

import dstu.csae.auth.graphic.dto.LoginRequest;
import dstu.csae.auth.graphic.dto.RegisterRequest;
import dstu.csae.auth.graphic.model.Account;
import dstu.csae.auth.graphic.model.PasswordHash;
import dstu.csae.auth.graphic.model.Profile;
import dstu.csae.auth.graphic.repository.AccountRepository;
import dstu.csae.auth.graphic.repository.PasswordHashRepository;
import dstu.csae.auth.graphic.repository.ProfileRepository;
import dstu.csae.auth.graphic.security.AccountDetailsImpl;
import dstu.csae.auth.graphic.security.JwtCore;
import dstu.csae.auth.graphic.service.AccountService;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class AuthController {

    private AccountRepository accountRepository;
    private PasswordHashRepository passwordHashRepository;
    private ProfileRepository profileRepository;
    private PasswordEncoder passwordEncoder;
    private AccountService accountService;
    private JwtCore jwtCore;

    @Autowired
    public  void setProfileRepository(ProfileRepository profileRepository){
        this.profileRepository = profileRepository;
    }

    @Autowired
    public void setPasswordHashRepository(PasswordHashRepository passwordHashRepository){
        this.passwordHashRepository = passwordHashRepository;
    }

    @Autowired
    public void setAccountRepository(AccountRepository accountRepository){
        this.accountRepository = accountRepository;
    }

    @Autowired
    public void setPasswordEncoder(PasswordEncoder passwordEncoder){
        this.passwordEncoder = passwordEncoder;
    }

    @Autowired
    public void setAccountService(AccountService accountService){
        this.accountService = accountService;
    }

    @Autowired
    public void setJwtCore(JwtCore jwtCore){
        this.jwtCore = jwtCore;
    }


    @PostMapping("/login")
    public ResponseEntity<?> loginUser(@RequestBody LoginRequest request, HttpServletResponse response){
        String identifier = request.getIdentifier();
        String password = request.getPassword();
        AccountDetailsImpl accountDetails = null;
        try{
            accountDetails = accountService.loadByIdentifier(identifier);
        }catch (UsernameNotFoundException ex){
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body("Неверный идентификатор");
        }catch (RuntimeException ex){
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body("Проблемы с учётной записью. Обратитесь к системному администратору");
        }
        if (accountDetails == null ||
                !passwordEncoder.matches(password, accountDetails.getPassword())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body("Неверный идентификатор или пароль");
        }
        UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(
                accountDetails, null, accountDetails.getAuthorities());
        String jwt2FA = jwtCore.generate2FaToken(authentication);

        Cookie cookie = new Cookie("jwt", jwt2FA);
        cookie.setHttpOnly(true);
        cookie.setSecure(true);
        cookie.setPath("/");
        cookie.setMaxAge(jwtCore.getLifetime2Fa());

        response.addHeader("Set-Cookie", String.format(
                "jwt=%s; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=%d",
                jwt2FA, jwtCore.getLifetime2Fa()));

        return ResponseEntity.ok(Map.of(
                "2fa_required", true,
                "redirect", "/two-factor"
        ));
    }

    @PostMapping("/register")
    public ResponseEntity<String> registerUser(@RequestBody RegisterRequest request) {
        if(accountRepository.existsByLogin(request.getLogin())){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Выберите другое имя пользователя");
        }
        if(accountRepository.existsByEmail(request.getMail())){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Пользователь с такой почтой уже зарегистрирован");
        }
        String hashed = passwordEncoder.encode(request.getPassword());
        Account account = new Account();
        Profile profile = new Profile();
        PasswordHash passwordHash = new PasswordHash();

        account.setLogin(request.getLogin());
        account.setEmail(request.getMail());
        account.setCreatedAt(LocalDateTime.now());
        profile.setAccount(account);
        profile.setFirstName(request.getFirstName());
        profile.setLastName(request.getLastName());
        profile.setBirthDate(request.getBirthDate());
        passwordHash.setCreatedAt(account.getCreatedAt());
        passwordHash.setAccount(account);
        passwordHash.setHash(hashed);
        passwordHash.setCreatedAt(account.getCreatedAt());
        accountRepository.save(account);
        passwordHashRepository.save(passwordHash);
        profileRepository.save(profile);
        return ResponseEntity.ok("Пользователь успешно зарегистрирован");
    }
}
