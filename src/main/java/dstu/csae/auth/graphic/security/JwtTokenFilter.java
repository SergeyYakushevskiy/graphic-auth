package dstu.csae.auth.graphic.security;

import dstu.csae.auth.graphic.service.AccountService;
import io.jsonwebtoken.ExpiredJwtException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import org.springframework.util.AntPathMatcher;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
public class JwtTokenFilter extends OncePerRequestFilter {
    private JwtCore jwtCore;
    private AccountService accountService;

    @Autowired
    public JwtTokenFilter(JwtCore jwtCore, AccountService accountService) {
        this.jwtCore = jwtCore;
        this.accountService = accountService;
    }

    @Bean
    public String[] publicPaths() {
        return new String[] {
                "/login",
                "/login.html",
                "/register",
                "/register.html",
                "/api/**",
                "/css/**",
                "/js/**",
                "/img/**",
                "/json/**"
        };
    }

    private boolean isPublicPath(String path) {
        AntPathMatcher pathMatcher = new AntPathMatcher();
        for (String pattern : publicPaths()) {
            if (pathMatcher.match(pattern, path)) {
                return true;
            }
        }
        return false;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {

        if (isPublicPath(request.getServletPath())) {
            filterChain.doFilter(request, response);
            return;
        }
        try {
            // 1. Попытка получить JWT из cookie
            String jwt = null;
            if (request.getCookies() != null) {
                for (var cookie : request.getCookies()) {
                    if ("jwt".equals(cookie.getName())) {
                        jwt = cookie.getValue();
                        break;
                    }
                }
            }

            // 2. Если из cookie не нашли, пробуем из заголовка Authorization
            if (jwt == null) {
                String headerAuth = request.getHeader("Authorization");
                if (headerAuth != null && headerAuth.startsWith("Bearer ")) {
                    jwt = headerAuth.substring(7);
                }
            }

            // 3. Проверяем и аутентифицируем пользователя по jwt
            if (jwt != null) {
                String identifier = null;
                try {
                    identifier = jwtCore.getNameFromJwt(jwt);
                } catch (ExpiredJwtException e) {
                    response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                    response.getWriter().write("JWT expired");
                    return;
                }
                if (identifier != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                    UserDetails userDetails = accountService.loadByIdentifier(identifier);
                    UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(
                            userDetails,
                            null,
                            userDetails.getAuthorities()
                    );
                    SecurityContextHolder.getContext().setAuthentication(auth);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        filterChain.doFilter(request, response);
    }
}
