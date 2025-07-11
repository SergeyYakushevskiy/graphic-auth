package dstu.csae.auth.graphic.config;

import dstu.csae.auth.graphic.security.JwtTokenFilter;
import dstu.csae.auth.graphic.security.SameSiteCookieFilter;
import dstu.csae.auth.graphic.service.AccountService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.Ordered;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.HttpStatusEntryPoint;
import org.springframework.security.web.authentication.LoginUrlAuthenticationEntryPoint;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    private final String[] publicPath;
    private final JwtTokenFilter tokenFilter;
    private final SameSiteCookieFilter cookieFilter;
    private final AccountService accountService;

    @Autowired
    public SecurityConfig(JwtTokenFilter tokenFilter, AccountService accountService,
                          SameSiteCookieFilter cookieFilter, String[] publicPath) {
        this.tokenFilter = tokenFilter;
        this.accountService = accountService;
        this.cookieFilter = cookieFilter;
        this.publicPath = publicPath;
    }



    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration configuration) throws Exception {
        return configuration.getAuthenticationManager();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .csrf(AbstractHttpConfigurer::disable)
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers(publicPath).permitAll()
                        .requestMatchers(HttpMethod.POST, "/api/**").permitAll()
                        .anyRequest().authenticated()
                )
                .exceptionHandling(eh -> eh
                        .authenticationEntryPoint(
                                (request, response, authException) -> response.sendRedirect("/login.html")
                        ))
                .addFilterBefore(tokenFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }

    @Bean
    public FilterRegistrationBean<SameSiteCookieFilter> sameSiteCookieFilterRegistration(SameSiteCookieFilter filter) {
        FilterRegistrationBean<SameSiteCookieFilter> registration = new FilterRegistrationBean<>(filter);
        registration.setOrder(Ordered.LOWEST_PRECEDENCE);
        return registration;
    }

}
