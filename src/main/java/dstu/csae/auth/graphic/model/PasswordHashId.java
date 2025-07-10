package dstu.csae.auth.graphic.model;

import java.io.Serializable;
import java.util.Objects;
import java.util.UUID;

// Класс для составного PK password_hash
public class PasswordHashId implements Serializable {
    private UUID account;
    private String hash;

    public PasswordHashId() {}

    public PasswordHashId(UUID account, String hash) {
        this.account = account;
        this.hash = hash;
    }

    // equals и hashCode
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof PasswordHashId)) return false;
        PasswordHashId that = (PasswordHashId) o;
        return Objects.equals(account, that.account) && Objects.equals(hash, that.hash);
    }

    @Override
    public int hashCode() {
        return Objects.hash(account, hash);
    }
}
